import axios from "axios";
import {handleMessage} from "@/api/utils.ts";

const axiosIns = axios.create({
    // baseURL: "http://localhost:8080"
    baseURL: "http://127.0.0.1:4523/m1/6187324-5879816-default"
})

export interface Explain {
    type: "definition" | "example" | "ext_link"
    content: string
}

export interface ParseResult {
    type: "ner" | "hard" | "ordinary"
    startInclusive: number
    endExclusive: number
    explains: Explain[]
}

export interface Result {
    type: "success" | "error" | "warning" | "info" | "none"
    code: number
    data: any
    msg: string
}

export async function getParseResults(text: string) {
    const resp = await axiosIns.post("/api/parse-result",
        {
            text: text
        }
    )

    if (resp.status !== 200) {
        handleMessage("error", `网络请求请求失败, code=${resp.status}`)
        return;
    }

    const result = resp.data as Result
    handleMessage(result.type, result.msg)
    if (result.code !== 200) {
        return;
    }

    return result.data as ParseResult[]

}



