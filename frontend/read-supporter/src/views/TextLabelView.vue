<template>
  <div class="wrapper">
    <n-spin :show="isLoading || isImportingArticle" style="height: 100%; width: 100%;" id="TextLabelView_Spin_0"
            size="large">
      <n-split direction="horizontal" style="height: 100%" :max="0.75" :min="0.5" :default-size="0.75">
        <template #1>
          <div class="textareaLayout">
            <n-input
                id="TextLabelView_input_0"
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
              <n-dropdown trigger="click" size="large" :options="summaryOptions" @select="onSelectSummaryOption"
                          :show-arrow="true">
                <n-image
                    width="200"
                    height="200"
                    :src="titlePic"
                    preview-disabled
                />
              </n-dropdown>
            </n-flex>
            <n-flex justify="center" align="center">
              <n-button type="primary" style="width: 150px; height: 50px;" @click="switchMode">
                <div v-if="isInputMode" class="btnClass">
                  Go Render
                </div>
                <div v-if="!isInputMode" class="btnClass">
                  Go Edit
                </div>
              </n-button>
              <n-button type="primary" style="width: 200px; height: 50px;" @click="switchImportModal">
                <div class="btnClass">
                  Import Article
                </div>
              </n-button>
            </n-flex>
            <n-flex vertical justify="center" align="center" style="margin: 10px 10px 10px 10px;">
              <n-input id="TextLabelView_input_1"
                       v-model:value="summary"
                       type="textarea"
                       placeholder="Summary..."
                       round
                       readonly
                       :style="{
                          'width': '100%',
                          'height': '100%',
                          'resize': 'none',
                          'font-size': '25px',
                          'font-family': `${fontFamily}`,
                       }
              ">

              </n-input>
            </n-flex>
          </div>
        </template>
      </n-split>
      <n-modal v-model:show="showImportModal">
        <n-card title="Import Article From URL" style="width: 50%; height: 50%;">
          <n-form
              ref="importFormRef"
              :model="importFormValue"
              :rules="importFormRules"
              size="large"
          >
            <n-form-item label="URL" path="importUrl">
              <n-input v-model:value="importFormValue.importUrl" placeholder="please input your import article's url."/>
            </n-form-item>
            <n-flex justify="center" align="center">
              <n-button type="primary" style="width: 150px; height: 50px;" @click="importArticle">
                <div class="btnClass">
                  import
                </div>
              </n-button>
            </n-flex>
          </n-form>
        </n-card>
      </n-modal>
    </n-spin>
  </div>
</template>


<script setup lang="ts">
import {type Ref, ref, h, type Component} from 'vue'
import titlePic from '@/assets/anime_girl.png'
import {fetchArticle, getParseResults, getSummary} from '@/api/backend.ts'
import type {ParseResult} from '@/api/backend.ts'
import {useMessage, NIcon} from "naive-ui";
import type {FormInst} from 'naive-ui'
import SingleTextSnippet from "@/components/SingleTextSnippet.vue";
import {Checkmark} from '@vicons/ionicons5'

const _window = window as any
_window.$message = useMessage()

const isInputMode = ref(true)
const article = ref('')
const summary = ref('')
const fontFamily = "Menlo, Consolas, Monaco, 'Lucida Console', 'Liberation Mono', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Courier New', monospace, serif"
const isLoading = ref(false)

function switchMode() {
  isInputMode.value = !isInputMode.value
  if (!isInputMode.value) {
    getRenderedText()
  }
}

const renderedParseResults = ref<ParseResult[]>([])

function reset() {
  renderedParseResults.value = []
  summary.value = ''
}

async function getRenderedText() {
  isLoading.value = true
  reset()
  let parseResults: ParseResult[] | undefined = [];
  let summaryRespText: string | undefined = ''
  try {
    [parseResults, summaryRespText] = await Promise.all([
      getParseResults(article.value),
      getSummary(article.value, summaryOption.value)
    ]);
  } catch (e) {
    _window.$message.error(`Failed to get parse results: ${e}`)
    console.log(e)
    isLoading.value = false
    return;
  }

  if (!parseResults || !summaryRespText) {
    isLoading.value = false
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
  summary.value = summaryRespText

  isLoading.value = false
}

const showImportModal = ref(false)
const importFormRef: Ref<FormInst | null> = ref<FormInst | null>(null)
const importFormValue = ref({
  importUrl: '',
})
const importFormRules = {
  importUrl: {
    required: true,
    message: 'please input a valid URL',
    trigger: 'blur',
    type: 'url',
  }
}
const isImportingArticle = ref(false)

function switchImportModal() {
  showImportModal.value = !showImportModal.value
}

async function importArticle(e: MouseEvent) {
  e.preventDefault()
  try {
    await importFormRef.value?.validate()
  } catch (err) {
    console.log(e)
    return;
  }

  isImportingArticle.value = true
  const url = importFormValue.value.importUrl
  const fetchedArticle = await fetchArticle(url)
  if (!fetchedArticle) {
    _window.$message.error(`Failed to fetch article: ${url}`)
    isImportingArticle.value = false
    return;
  }

  article.value = fetchedArticle
  isInputMode.value = true
  showImportModal.value = false
  isImportingArticle.value = false
}

const summaryOption = ref('lda')
const summaryOptions = [
  {
    label: 'Summarize With Bart',
    key: 'bart',
    icon: renderIcon(Checkmark, 'bart'),
  },
  {
    label: 'Summarize With LDA',
    key: 'lda',
    icon: renderIcon(Checkmark, 'lda'),
  },
  {
    label: 'Summarize With LSA',
    key: 'lsa',
    icon: renderIcon(Checkmark, 'lsa'),
  },
  {
    label: 'Summarize With Textrank',
    key: 'textrank',
    icon: renderIcon(Checkmark, 'textrank'),
  }
]

function renderIcon(icon: Component, key: string) {
  return () => {
    return h(NIcon,
        {
          color: key === summaryOption.value ? "rgba(41, 198, 41, 1)" : "rgba(0, 255, 0, 0)",
          size: "large",
        }, {
          default: () => h(icon)
        })
  }
}

function onSelectSummaryOption(key: string) {
  summaryOption.value = key
}

</script>

<style>
#TextLabelView_input_0 .n-input-wrapper {
  resize: none;
}

#TextLabelView_input_1 .n-input-wrapper {
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
  grid-template-rows: 220px 1fr 500px;
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