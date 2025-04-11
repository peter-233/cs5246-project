<template>
<div v-for="explain in sortedExplains"
     :style="{
       'font-family': `${fontFamily}`,
       'font-size': '15px',
       'min-width': '300px',
     }">
  <h3>{{explainTitle[explain.type]}}</h3>
  <a v-if="explain.type === 'ext_link'" :href="explain.content" >
    {{explain.content}}
  </a>
  <div v-else>
    {{explain.content}}
  </div>
  <n-divider/>
</div>
</template>

<script setup lang="ts">
import type {Explain} from "@/api/backend.ts";

const props = defineProps<{
  explains: Explain[]
}>()

const fontFamily = "Menlo, Consolas, Monaco, 'Lucida Console', 'Liberation Mono', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Courier New', monospace, serif"
const explainSequence = {
  'definition': 1,
  'example': 2,
  'ext_link': 3,
  'ner_label': 4,
}
const explainTitle = {
  'definition': 'Definition',
  'example': 'Example',
  'ext_link': 'External Link',
  'ner_label': 'Name Entity Recognition Label',
}
const sortedExplains = [...props.explains]
sortedExplains.sort((lhs, rhs) => {
  return explainSequence[lhs.type] - explainSequence[rhs.type]
})




</script>

<style scoped>

</style>