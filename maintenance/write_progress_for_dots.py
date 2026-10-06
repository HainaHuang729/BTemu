"""Read development status metadata and publish a monitoring snapshot; no submissions."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]

def read(root, name):
    return json.loads((root / name).read_text())

def atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp.' + str(os.getpid()))
    tmp.write_text(text)
    os.replace(str(tmp), str(path))

def main(root):
    now = time.time()
    state = read(root, 'data_runs/20261001_batch2/continuation_status.json')
    recovered = read(root, 'manifests/qualified_history_recovered_v1.json')
    initial = len({r['sample_id'] for r in recovered['files'] if r['split'] == 'train'})
    curve = read(root, 'artifacts/learning_curve_fixed_validation_v1/status.json')
    audit = read(root, 'results/endpoint_domain_audit.json')
    qualification = read(root, 'results/native_qualification.json')
    alerts = []
    if now - state['as_of_unix'] > 7200:
        alerts.append('生产汇总超过 2 小时未刷新；检查队列和 worker 日志，不自动取消作业。')
    job = state.get('submitted_job')
    jobs, queue_error = [], None
    if job:
        try:
            r = subprocess.run(['squeue', '-j', str(job), '-h', '-o', '%i|%T|%N|%C|%R'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=15)
            if r.returncode:
                queue_error = r.stderr.strip()
            else:
                for line in r.stdout.splitlines():
                    fields = line.split('|', 4)
                    if len(fields) == 5:
                        jobs.append(dict(zip(['job_id','state','nodes','cpus','reason'], fields)))
        except (OSError, subprocess.TimeoutExpired) as error:
            queue_error = str(error)
    if queue_error:
        alerts.append('队列读取失败；作业实际状态未知。')
    datasets = {}
    for split, planned in [('train', 4096), ('validation', 512)]:
        t = state['table'][split]
        qualified = t['qualified'] + (initial if split == 'train' else 0)
        datasets[split] = {'planned': planned, 'qualified': qualified, 'remaining_unqualified': planned-qualified,
            'batch2_attempts': t['attempts'], 'batch2_failed': t['failed'], 'initial_train_qualified': initial if split == 'train' else 0}
        if t['failed']:
            alerts.append(split + ' 有失败记录，按类型归纳；不能重抽或修改物理配置。')
        if audit['by_split'][split]['count'] != qualified:
            alerts.append(split + ' endpoint 汇总与生产汇总数量暂不一致，可能处于更新窗口。')
    if not qualification.get('qualified_for_batch1'):
        alerts.append('native qualification 未通过；需要检查既有验收记录。')
    stamp = datetime.datetime.fromtimestamp(now, datetime.timezone(datetime.timedelta(hours=8))).isoformat()
    snapshot = {'schema_version': 1, 'updated_at_hkt': stamp, 'source_updated_at_unix': state['as_of_unix'],
        'source_age_seconds': round(now-state['as_of_unix']), 'production_status': state['status'],
        'datasets': datasets, 'last_submitted_job': job, 'queue_snapshot': jobs, 'queue_error': queue_error,
        'native_qualified': bool(qualification.get('qualified_for_batch1')), 'learning_curve': curve,
        'endpoint_audit': audit, 'alerts': alerts,
        'accounting': {'scope': '20261001_batch2 only; excludes initial448/preflight/training',
            'charged_core_hours_as_reported': state['charged_core_hours'], 'reserved_core_hours_as_reported': state['reserved_core_hours']},
        'sealed_labels_read_by_monitor': False, 'production_mcmc_started_by_monitor': False}
    atomic(root/'results/dots_progress.json', json.dumps(snapshot, ensure_ascii=False, indent=2)+'\n')
    lines = ['# BT 10D xHI Emulator 进度（dots 监控入口）', '',
        '更新时间：'+stamp+'。此文档为刷新时的快照，生产侧汇总距刷新 '+str(snapshot['source_age_seconds'])+' 秒。', '',
        '当前阶段：`'+state['status']+'`。正式数据仍在生产；首轮模型完成开发训练，但尚未达到科学部署要求。', '',
        '| Dataset | Planned | Qualified | Remaining unqualified | Batch2 failed |',
        '|---|---:|---:|---:|---:|']
    for split, t in datasets.items():
        lines.append('| '+split+' | '+str(t['planned'])+' | '+str(t['qualified'])+' | '+str(t['remaining_unqualified'])+' | '+str(t['batch2_failed'])+' |')
    lines += ['', 'Train 合格数包含首批 '+str(initial)+' 条已验收 history；Batch2 attempts/failed 不包含首批历史重试记录。剩余未合格不等于尚未提交。', '',
        '## 当前队列', '', '最近提交作业：`'+str(job)+'`。仅列最近一波的即时队列状态；空表不代表完成，需查 receipts 与 sacct。', '',
        '| Job | Slurm state | Node | CPU | Reason |', '|---|---|---|---:|---|']
    for row in jobs:
        lines.append('| '+' | '.join(row[k].replace('|','/') for k in ['job_id','state','nodes','cpus','reason'])+' |')
    if not jobs:
        lines.append('| — | UNKNOWN（队列读取失败） | — | — | — |' if queue_error else '| — | 当前队列无该作业；终态待核对 | — | — | — |')
    lines += ['', '资源：仅使用 tkcastrosim1 / chpc-cn[057-064]，最多 8 个完整 evaluations 并发，单任务最多 16 CPU、16 GiB、2 小时。总 core-hour 上限已由用户取消；尝试次数和单任务限制仍有效。', '',
        'Batch2 汇总记账：已计入 %.3f core-hours，预留 %.3f core-hours。此数不含首批 448、preflight、模型训练，且以生产侧记账时间为准。' % (state['charged_core_hours'], state['reserved_core_hours']), '',
        '## 科学对象和验收边界', '',
        '- 10D 输入；fixed-IC requested seed 725213656658；32 节点体积平均 global_xHI。',
        '- Selected native SHA256：`3211a6629109da7379694a9fefeb685b93b71d225f7fdf54120818a94e5702b2`。既有 native/adapter/PL 极限预检已通过。',
        '- τ 完全由原 history 后处理派生；LF 保留原精确 forward。',
        '- z=5 中性残余和 z=35 早期电离属于 SCIENCE_DOMAIN_WARNING，不删标签、不强制完全电离。',
        '- LF-invalid 但 history-valid 的标签仍可用于 history 训练；不宣称该点 joint likelihood 有效。',
        '- 45 条旧隔离记录未转入训练。封存测试未开启；监控器不读取封存文件或标签。不启动生产 MCMC。', '',
        '## 开发训练', '',
        '首轮使用固定 1024 Train / 144 Validation、5 个初始化 seeds，已完成。Ensemble trajectory RMSE q95=0.18746；|Δτ| q90=0.02316，当前不足以用于科学推断。', '',
        '训练误差下降但验证改善不足。验证误差与最近训练点距离相关系数约 0.095，尚不能确定主要原因。', '',
        '| Train N | 状态 |', '|---:|---|']
    for row in curve['milestones']:
        lines.append('| '+str(row['N'])+' | '+row['status']+' |')
    lines += ['', '2048/4096 达到冻结样本要求后由现有 controller 自动提交；固定首轮 144 Validation、同一配置和全部 5 seeds。上述 WAITING 状态表示尚未提交训练作业。', '',
        '## Endpoint 与组件有效性（开发数据）', '',
        '| Split | History-valid | LF-invalid/history-valid | xHI(5) q50 / q95 | xHI(35) q50 / min |', '|---|---:|---:|---|---|']
    for split,a in audit['by_split'].items():
        lines.append('| %s | %s | %s | %.6f / %.6f | %.6f / %.6f |' % (split,a['history_valid_count'],a['LF_invalid_but_history_valid_count'],a['xHI_zmin']['q50'],a['xHI_zmin']['q95'],a['xHI_zmax']['q50'],a['xHI_zmax']['min']))
    lines += ['', '真实 numerical failure count（开发侧 QA 汇总）：'+str(audit['true_numerical_failure_count'])+'。更多分位数和阈值计数见 results/endpoint_domain_audit.json。', '',
        '## dots 刷新与告警规则', '',
        '固定入口：`docs/progress_for_dots.md`；机器入口：`results/dots_progress.json`。生产状态源由现有流水线更新；本快照由下列命令刷新。dots 可每 10–15 分钟调用，不需要完整模拟环境：', '',
        '```bash', 'python3 '+str(root/'maintenance/write_progress_for_dots.py'), '```', '',
        '刷新命令只读取开发状态、汇总 metadata 和 Slurm 队列，原子写入两个监控文件；不提交或取消作业，不读 sealed labels，不改科学契约或生产代码。未新建定时任务；dots 需调用上述命令获得新快照。', '',
        '- source_age_seconds > 7200：检查是否超时、等待调度或汇总失败；不要仅凭时间自动取消。',
        '- PENDING 仅表示等待；RUNNING 才表示执行中。最近作业不在队列时检查 sacct 和验收回执。',
        '- 数量不增长且无运行/等待作业：检查 continuation_status、失败 registry 与 controller 错误文件。',
        '- 偶发独立失败按既有协议记录后继续其他点；系统性 native/config/provenance 错误应人工核查。',
        '- Endpoint warnings 与 LF-domain failures 不触发删除 history。不得自动改 seed、native、分辨率、priors 或 split。', '',
        '本次告警：']
    lines += ['- '+a for a in alerts] if alerts else ['- 无。']
    lines += ['', '关键证据路径：', '',
        '- `data_runs/20261001_batch2/continuation_status.json`、`failure_registry.json`、`submissions.jsonl`',
        '- `results/native_qualification.json`、`results/endpoint_domain_audit.json`',
        '- `artifacts/learning_curve_fixed_validation_v1/status.json`',
        '- `artifacts/development_history_fidelity_20261003/diagnostics/trajectory_diagnostics.json`', '',
        '下一步：继续冻结 Train4096 / Validation512 生产；依次完成 2048 与 4096 learning curve；之后检查 history、派生 τ/xHI 和各项 likelihood fidelity。最终封存验收仍需单独授权。', '']
    v2_path=root/'results/dataset_progress.json'
    if v2_path.exists():
        v2=read(root,'results/dataset_progress.json')
        lines += ['## Dataset v2 100k（独立生产）', '',
            'v2快照更新时间：'+str(v2.get('updated_at_hkt',v2['updated_at_unix']))+'。更多实时字段见 results/dataset_progress.json；执行记录见 docs/dataset_v2_100k_production.md。', '',
            'Train：'+str(v2['datasets']['train']['qualified'])+'/100000（已包含截至该快照的合格v1 Train）；独立 Validation v2：'+str(v2['datasets']['validation']['qualified'])+'/10000。旧Validation512继续保留v1 benchmark。', '',
            'v2 RUNNING='+str(v2.get('running','UNKNOWN'))+'，PENDING='+str(v2.get('pending','UNKNOWN'))+'；当前ramp='+str(v2['current_ramp_concurrency'])+'，配置上限='+str(v2['max_array_concurrency'])+'。', '',
            'v2 true numerical failures='+str(v2.get('numerical_failed','UNKNOWN'))+'；stop reasons='+str(v2['stop_reasons'])+'。sealed v2只有独立参数设计，未生成/读取labels。', '']
    atomic(root/'docs/progress_for_dots.md', '\n'.join(lines))
    print(json.dumps({'document':str(root/'docs/progress_for_dots.md'),'datasets':datasets,'alerts':alerts},ensure_ascii=False))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', type=Path, default=ROOT)
    main(parser.parse_args().project)
