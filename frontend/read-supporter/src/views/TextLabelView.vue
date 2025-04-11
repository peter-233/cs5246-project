<template>
  <div class="wrapper">
    <n-spin :show="isLoading" style="height: 100%; width: 100%;" id="TextLabelView_Spin_0" size="large">
      <n-split direction="horizontal" style="height: 100%" :max="0.75" :min="0.5" :default-size="0.75">
        <template #1>
          <div class="textareaLayout" id="TextLabelView_textareaLayout_0">
            <n-input
                v-if="isInputMode"
                v-model:value="article"
                type="textarea"
                placeholder="Input your text here"
                round
                clearable
                :style="{
                'width': '100%',
                'height': '100%',
                'resize': 'none',
                'font-size': '25px',
                'font-family': `${fontFamily}`,
              }"
            />
            <div
                v-if="!isInputMode"
                style="height: 100%; width: 100%; border: 1px solid black;
                border-radius: 5px;
                display: block; word-break: normal; overflow-wrap: break-word;"
            >
              <n-scrollbar>
                <SingleTextSnippet :type="result.type"
                                   :snippet="article.substring(result.startInclusive, result.endExclusive)"
                                   :explains="result.explains" v-for="result in renderedParseResults"/>
              </n-scrollbar>

            </div>
          </div>
        </template>
        <template #2>
          <div class="gridLayout">
            <n-flex justify="center" align="center">
              <n-image
                  width="200"
                  height="200"
                  :src="titlePic"
                  preview-disabled
              />
            </n-flex>
            <n-flex vertical justify="center" align="center">
              <n-button type="primary" style="width: 200px; height: 50px;" @click="switchMode">
                <div v-if="isInputMode" class="btnClass">
                  Go Render
                </div>
                <div v-if="!isInputMode" class="btnClass">
                  Go Edit
                </div>
              </n-button>
            </n-flex>
          </div>
        </template>
      </n-split>
    </n-spin>
  </div>
</template>


<script setup lang="ts">
import {ref} from 'vue'
import titlePic from '@/assets/anime_girl.png'
import {getParseResults} from '@/api/backend.ts'
import type {ParseResult} from '@/api/backend.ts'
import {useMessage} from "naive-ui";
import SingleTextSnippet from "@/components/SingleTextSnippet.vue";

// noinspection TypeScriptUnresolvedReference
const _window = window as any
_window.$message = useMessage()

const isInputMode = ref(true)
const article = ref('')
const fontFamily = "Menlo, Consolas, Monaco, 'Lucida Console', 'Liberation Mono', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Courier New', monospace, serif"
const isLoading = ref(false)

function switchMode() {
  isInputMode.value = !isInputMode.value
  if (!isInputMode.value) {
    getRenderedText()
  }
}

const renderedParseResults = ref<ParseResult[]>([])

async function getRenderedText() {
  isLoading.value = true
  let parseResults: ParseResult[] | undefined = [];

  try {
    parseResults = await getParseResults(article.value)
  } catch (e) {
    _window.$message.error(`Failed to get parse results: ${e}`)
    console.log(e)
    isLoading.value = false
    return;
  }

  if (!parseResults) {
    return;
  }

  parseResults.sort((lhs, rhs) => {
    return lhs.startInclusive - rhs.startInclusive
  })
  let lastEnd = 0
  let newRenderedParseResults: ParseResult[] = []
  for (const result of parseResults) {
    newRenderedParseResults.push({
      startInclusive: lastEnd,
      endExclusive: result.startInclusive,
      type: 'ordinary',
      explains: [],
    })
    if (result.type) {
      newRenderedParseResults.push(result)
    }
    lastEnd = result.endExclusive
  }
  newRenderedParseResults.push({
    startInclusive: lastEnd,
    endExclusive: article.value.length,
    type: 'ordinary',
    explains: [],
  })
  renderedParseResults.value = newRenderedParseResults

  isLoading.value = false
}

</script>

<style>
#TextLabelView_textareaLayout_0 .n-input-wrapper {
  resize: none;
}

#TextLabelView_Spin_0 .n-spin-content {
  height: 100%;
  width: 100%;
}

</style>

<style scoped>
.wrapper {
  width: 100%;
  height: 100%;
}

.gridLayout {
  display: grid;
  grid-template-rows: 300px 1fr;
  width: 100%;
  height: 100%;
}

.textareaLayout {
  margin: 20px;
  height: calc(100% - 40px);
  width: calc(100% - 40px);
}

.btnClass {
  font-size: 20px;
  font-weight: bold;
}

</style>