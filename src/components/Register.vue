<template>
<b-container fluid>
    <div class="row"></div>
    <div class="row">
        <div class="col-md-4"></div>
        <div class="col-md-4">
            <b-form @submit.prevent="onSubmit" @reset.prevent="onReset" v-if="show">
            <b-form-group
                label="Email address:">
                <b-form-input
                v-model="form.email"
                type="email"
                required
                placeholder="Enter email"
                ></b-form-input>
            </b-form-group>

            <div class="error" v-html="error" />

            <b-form-group label="Your password:">
                <b-form-input
                v-model="form.password"
                required
                placeholder="Enter password"
                ></b-form-input>
            </b-form-group>

            <b-form-group label="Birth:">
                <b-form-input
                v-model="form.birth"
                required
                type="date"
                ></b-form-input>
            </b-form-group>

            <b-form-group>
              <b-form-radio-group v-model="form.gender">
              <b-form-radio value="male">Male</b-form-radio>
              <b-form-radio value="female">Female</b-form-radio>
              </b-form-radio-group>
            </b-form-group>

            <b-button type="submit" style="margin-right:5px" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
            </b-form>            
        </div>
    </div>
</b-container>
</template>

<script>
import api from '../api'
  export default {
    data() {
      return {
        form: {
          email: '',
          password: '',
          birth: null,
          gender: []
        },
        error: '',
        show: true
      }
    },
    methods: {
      async onSubmit() {
        try {
          const res = await api.register(this.form)
          alert(res.data.message)
        } catch(error) {
          console.log(error)
          this.error = error.response.data.error
        }
      },

      onReset() {
        // Reset our form values
        this.form.email = ''
        this.form.password = ''
        this.form.birth = null
        this.form.gender = []
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>

<style>
    .row {
        margin-top: 24px;
        margin-bottom: 24px;
    }
    .error {
      color:red
    }
    b-button {
      margin-right: 5px
    }
</style>