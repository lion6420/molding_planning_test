<template>
  <v-bottom-navigation
    v-model="bottomNav"
  >
    <!-- <img src="../img/Logo.png">
    <img src="../img/fii_icon.png"> -->
    <v-spacer/>

    <v-btn>
      <span class="text-custom">操作手冊</span>
    </v-btn>

    <v-btn>
      <span class="text-custom">招募團隊</span>
    </v-btn>

    <v-btn>
      <span class="text-custom">最新公告</span>
    </v-btn>

    <v-btn href="http://localhost:8080/login" v-if="showLogin">
      登入
    </v-btn>
    <v-btn v-if="showRegister" href="http://localhost:8080/register">
      註冊
    </v-btn>
    
    <v-btn v-if="showProfile" @click="goProfile">
      帳戶資訊
    </v-btn>
    <v-btn v-if="showLogout" @click="logout">
      登出
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
export default {
  data() {
    if(localStorage.getItem('user-token')) {
      return {
        showLogin:false,
        showRegister:false,
        showProfile:true,
        showLogout:true,
        }
    }
    else {
      return {
        showLogin:true,
        showRegister:true,
        showProfile:false,
        showLogout:false,
        }
    }
  },

  methods: {
    goProfile () {
      const userId = localStorage.getItem('user-id')
      this.$router.push('/profile?id=' + userId)
    },
    logout () {
      localStorage.removeItem('user-id')
      localStorage.removeItem('user-token')
      localStorage.removeItem('user-name')
      this.$router.push('/')
      this.$router.go(0)
    }
  }
}
</script>

<style>
  .text-custom {
    font-weight:bold;
  }
</style>