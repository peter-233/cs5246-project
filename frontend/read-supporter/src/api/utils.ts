export function handleMessage(type: string, msg: string) {
    if(type === "success") {
        window.$message.success(msg)
    } else if(type === "error") {
        window.$message.error(msg)
    } else if(type === "warning") {
        window.$message.warning(msg)
    } else if(type === "info") {
        window.$message.info(msg)
    } else if (type === "none") {
        // pass
    } else {
        window.$message.error("Unknown message type: " + type)
        throw new Error("Unknown message type: " + type)
    }
}