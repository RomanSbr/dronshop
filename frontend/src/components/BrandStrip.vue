<template>
  <div class="brands">
    <div class="section-head"><div class="title">Популярные бренды</div></div>
    <div class="row wrap gap16">
      <div v-for="b in brands" :key="b" class="brand pill">{{ b }}</div>
    </div>
  </div>
</template>

<script setup>
const brands = ['DJI','GepRC','RadioMaster','Gemfan','BetaFPV','iFlight','HDZero','Walksnail']
</script>

<style scoped>
.brands{ margin-top: 28px; }
.section-head .title{ font-weight: 600; }
.row{ display:flex; }
.wrap{ flex-wrap: wrap; }
.gap16{ gap: 16px; }
.brand{ padding: 8px 10px; background:#fff; border:1px solid #eef2f7; }
</style>

