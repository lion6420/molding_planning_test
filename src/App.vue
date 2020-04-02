<template>
  <div id="app">
    <nav-top/>
    <nav-bar/>
    <router-view/>
  </div>
</template>

<script>
import NavTop from './components/NavBar-Top'
import NavBar from './components/NavBar'

export default {
  name: 'App',
  components: {
    NavTop,
    NavBar
  }
}
</script>

<style>
</style>
