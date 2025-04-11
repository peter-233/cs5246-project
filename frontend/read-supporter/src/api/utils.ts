export function handleMessage(type: string, msg: string) {
    let _window = window as any;
    if(type === "success") {
        _window.$message.success(msg)
    } else if(type === "error") {
        _window.$message.error(msg)
    } else if(type === "warning") {
        _window.$message.warning(msg)
    } else if(type === "info") {
        _window.$message.info(msg)
    } else if (type === "none") {
        // pass
    } else {
        _window.$message.error("Unknown message type: " + type)
        throw new Error("Unknown message type: " + type)
    }
}