<template>
  <nav id="navBase">
    <a><router-link class="routerlink" to="/">首頁</router-link></a>
    <a><router-link class="routerlink" to="/planningresult">排配結果</router-link></a>
    <a><router-link class="routerlink" to="/weekly">需求列表</router-link></a>
    <a><router-link class="routerlink" to="/machine">機台狀態</router-link></a>
    <a><router-link class="routerlink" to="/bigselect">大表</router-link></a>
    <a><router-link class="routerlink" to="/test">測試</router-link></a>
    <a><router-link class="routerlink" to="/">測試</router-link></a>
    <a class="link" href="#">測試</a>
  </nav>
</template>

<script>
</script>

<style>
  #navBase {
    padding: 10px;
    text-align: center;
    font-family: "Microsoft JhengHei";
    background: black;
  }
  .link, .routerlink {
    color: #ffffff;
    font-size: 15px;
    padding: 0 30px;
  }
  .routerlink:hover, .link:hover {
    background-color: red;
    color: white;
    text-decoration: none;
    padding: 10px 30px;
  }
  .router-link-exact-active {
    background-color: red;
    color: white;
    padding: 10px 30px;
  }
</style>