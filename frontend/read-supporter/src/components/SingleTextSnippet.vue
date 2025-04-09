<template>
  <template v-if="props.type === 'ordinary'">
    <span :style="ordinaryRenderedTextStyle">{{ props.snippet }}</span>
  </template>
  <template v-if="props.type === 'hard'">
    <n-popover trigger="hover">
      <template #trigger>
        <span :style="hardRenderedTextStyle">{{ props.snippet }}</span>
      </template>
      <ExplainPanel :explains="props.explains"/>
    </n-popover>
  </template>
  <template v-if="props.type === 'ner'">
    <n-popover trigger="hover">
      <template #trigger>
        <span :style="nerRenderedTextStyle">{{ props.snippet }}</span>
      </template>
      <ExplainPanel :explains="props.explains"/>
    </n-popover>
  </template>
</template>

<script setup lang="ts">
import type {Explain} from "@/api/backend.ts";
import ExplainPanel from "@/components/ExplainPanel.vue";

const props = defineProps<{
  type: "hard" | "ner" | "ordinary"
  snippet: string
  explains: Explain[]
}>()

const fontFamily = "Menlo, Consolas, Monaco, 'Lucida Console', 'Liberation Mono', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Courier New', monospace, serif"


const hardRenderedTextStyle = `
  background-color: rgba(250, 6, 49, 0.8);
  border-radius: 3px;
  font-family: ${fontFamily};
  white-space: pre-wrap;
  font-size: 25px;
  display: inline;
`.trim();
const nerRenderedTextStyle = `
  background-color: rgba(253, 120, 3, 0.8);
  border-radius: 3px;
  font-family: ${fontFamily};
  white-space: pre-wrap;
  font-size: 25px;
  display: inline;
`.trim();
const ordinaryRenderedTextStyle = `
  font-family: ${fontFamily};
  white-space: pre-wrap;
  font-size: 25px;
  display: inline;
`.trim();

</script>


<style scoped>

</style>