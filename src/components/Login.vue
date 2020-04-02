<template>
<b-container fluid>
    <div class="row" style="margin-top:24px">
      <div class="col-md-4"></div>
      <div class="col-md-4">
        <b-form @submit.prevent="Login" v-if="show">
        <b-form-group label="Email address:">
            <b-form-input
            v-model="form.email"
            type="email"
            required
            placeholder="Enter email"
            ></b-form-input>
        </b-form-group>

        <b-form-group label="Your password:">
            <b-form-input
            v-model="form.password"
            required
            placeholder="Enter password"
            ></b-form-input>
        </b-form-group>

        <b-button type="submit" style="margin-right:5px" variant="primary">Login</b-button>
        <b-button variant="danger">Forget password</b-button>
        </b-form>
      </div>
    </div>
  </b-container>
  </template>

  <script>
    export default {
      data() {
        return {
          form: {
            email: '',
            password: ''
          },
          show: true
        }
      },
      methods: {
          Login: function() {
            let data = {
              email: this.form.email,
              password: this.form.password
            }
            this.$store.dispatch('login', data)
            .then((response) => {
              console.log(response)
              alert(response.data.message)
              this.$router.push('/')
              this.$router.go(0)
            })
          .catch (err => {
            console.log(err)
          })
        }
      }
    }
  </script>
  <style>

  </style>