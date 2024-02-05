<script lang="ts" setup>
import { computed } from "vue"
import { Solar, Lunar } from "lunar-typescript"
import { getUserInfo } from "@/utils/cache/cookies"

const userInfo = getUserInfo()

// 欢迎语
const hello = computed(() => {
  let sentence = ""
  const now = new Date().getHours()
  if (now > 0 && now <= 6) {
    sentence = "午夜好，"
  } else if (now > 6 && now <= 11) {
    sentence = "早上好，"
  } else if (now > 11 && now <= 14) {
    sentence = "中午好，"
  } else if (now > 14 && now <= 18) {
    sentence = "下午好，"
  } else {
    sentence = "晚上好，"
  }
  return sentence + userInfo.username
})

//日期、节日、节气
const dayInfo = computed(() => {
  //阳历
  let solar = Solar.fromDate(new Date())
  let day = solar.toString()
  let week = solar.getWeekInChinese()
  //阴历
  let lunar = Lunar.fromDate(new Date())
  let lunarMonth = lunar.getMonthInChinese()
  let lunarDay = lunar.getDayInChinese()
  //节气
  let jieqi = lunar.getPrevJieQi().getName()
  let next = lunar.getNextJieQi()
  let nextJieqi = next.getName() + " " + next.getSolar().toYmd()

  return `${day} 星期${week}，农历${lunarMonth}${lunarDay}（当前${jieqi}，${nextJieqi} ）`
})
</script>

<template>
  <div class="user-header">
    <el-row>
      <el-col :span="15" style="font-size: var(--el-font-size-extra-large)">{{ hello }}</el-col>
      <el-col :span="9">{{ dayInfo }}</el-col>
    </el-row>
    <el-row>
      <el-col :span="15">
        <img src="@/assets/images/line-font.png" style="max-width: 60%; padding-left: 30px" />
      </el-col>
      <el-col :span="9">
        <div class="weather">
          <iframe
            width="100%"
            scrolling="no"
            height="50"
            frameborder="0"
            allowtransparency="true"
            src="//i.tianqi.com/index.php?c=code&id=12&icon=1&num=3&site=12"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 4px;
}

.user-header {
  width: 100%;
  background-color: #fff;
  margin-bottom: 10px;

  .weather {
    width: 400px;
  }
}
</style>
