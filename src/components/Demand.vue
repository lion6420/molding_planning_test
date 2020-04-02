<template>
<b-container fluid>
  <el-tabs
    text-align="center"
    v-model="tabName" 
    @tab-click="handleClick">
    <el-tab-pane label="週需求" name="weekly">
      <router-view/>
    </el-tab-pane>
    <el-tab-pane label="急件列表" name="emergency">
      <router-view/>
    </el-tab-pane>
  </el-tabs>
</b-container>
</template>

<script>
export default {
  data() {
    return {
      tabName: 'weekly'
    }
  },
  methods: {
    handleClick () {
      this.$router.push({name: this.tabName})
    }
  },
  mounted() {
    this.$router.push({name: this.tabName})
  }
}
</script>

<style>
  .el-tabs {
    font-family: "Microsoft JhengHei";
    /* font-weight: 700; */
  }
  .el-tab-pane {
    font-family: "Microsoft JhengHei";
  }
</style>