# 王清源｜H2D 与摄像头接口核对

已知：团队确认存在运行状态读取接口；本次补齐实际查到的字段、授权和资料链接，未实测项仍标待核对。首版只读，不依据这个接口的存在推断可以远程锁机。状态缺失或过期时按未知处理。

| 待核对 | 记录方式 |
|---|---|
| 能否区分空闲与打印中 | 可区分。社区整理的 MQTT 协议中 `print.gcode_state` 取值 `IDLE/RUNNING/PAUSE/FAILED/FINISH`，`IDLE` 为空闲、`RUNNING` 为打印中。H2D 真机字段取值待现场核对。 |
| 可用授权和网络边界 | 用「接入码 access code」接入：MQTT 认证为用户标识 + 接入码；可开局域网（LAN）模式做内网只读接入。由谁批准、适用设备和只读范围沿用协会流程，待确认。 |
| 摄像头可见范围 | 能只取设备区域。H2D 为内置喷嘴摄像头 + 腔体角落 live camera，只拍喷头/腔体/平台，不拍房间全景。人脸核验素材不进设备视觉流程。 |
| MCP 取帧 | 本项是 LabMate 自研 MCP 工具：输入有效会话 + 检查项，后端校验后输出设备区短时帧或不可用原因。无真机外部资料；引用 MCP 协议，待开发实现。 |
| 离线处理 | 离线时显示“状态未知”。后端管理准入，设备接口只读。为设计约定，待联调验证。 |

## 资料链接

- 拓竹 H2D 机型与固件：<https://bambulab.cn/zh-cn/support/firmware-download/h2d>
- H2D 智能检测与摄像头说明：<https://wiki.bambulab.com/en/h2/manual/intelligent-detection>
- 接入码接入（授权）：<https://wiki.bambulab.com/en/knowledge-sharing/access-code-connect>
- 局域网（LAN）模式（网络边界）：<https://wiki.bambulab.com/en/knowledge-sharing/enable-lan-mode>
- 拓竹 MQTT 状态协议（`gcode_state` 等字段）：<https://github.com/coelacant1/Bambu-Lab-Cloud-API/blob/main/API_MQTT.md>
- Model Context Protocol（MCP）：<https://modelcontextprotocol.io>

## 接入设计

- H2D 只读适配器：归一化状态为可用、忙碌或未知，附采集时间、来源和有效期限。过期或断连按未知处理，不进入检查通过。真实字段（`gcode_state`）与 H2D 实测取值待联调核对。
- 取帧工具：后端校验有效会话与检查项后，选择绑定的摄像头；只返回设备区域的临时画面或不可用原因。新手关键步骤可短时多帧，熟练用户默认按需触发。
- 视觉输入边界：只传设备画面、检查项和审核资料，隔离身份核验素材。摄像头异常（未安装／脏污／高温保护／未开启检测）提示无法判断并转现场核对。
- 接口字段、访问授权与采样参数已部分核对、部分待确认；禁止把模拟数据写成真机结果。
