<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <div class="navbar-brand mx-auto">
        <router-link to="/">
          <img src="../assets/logo1.png" alt="Logo" width="180" height="80" class="d-inline-block align-text-top" />
        </router-link>
      </div>
    </div>
  </nav>
  <main class="form-register w-50 m-auto">
    <form @submit.prevent="handleFormRegister">
      <!-- <img class="mb-4" src="../assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->
      <h1 class="h3 mb-3 fw-normal">Enroll yourself as Staff</h1>
      <div v-if="errStatus">
        <br />
        <p class="alert alert-danger">{{ errormsg }}</p>
      </div>
      <div class="form-floating mb-3">
        <input type="text" v-model="username" class="form-control" placeholder="username" />
        <label for="floatingInput">Username</label>
        <div class="error" v-if="v$.username.$error">Username is required</div>
      </div>
      <div class="form-floating mb-3">
        <input type="email" v-model="email" class="form-control" placeholder="email" />
        <label for="floatingInput">Email</label>
        <div class="error" v-if="v$.email.$error">
          Email is required.Enter in correct format
        </div>
        <!-- <div class="error" v-if="v$.email.email">
            Enter correct email format
          </div> -->
      </div>
      <div class="form-floating mb-3">
        <input type="password" v-model="password" class="form-control" id="floatingPassword" placeholder="Password" />
        <label for="floatingPassword">Password</label>
        <div class="error" v-if="v$.password.$error">
          Password is required and must be of minimum 5 characters.
        </div>
      </div>
      <div class="form-floating mb-3">
        <input type="password" v-model="repeatPassword" class="form-control" id="floatingPassword2"
          placeholder="Password" />
        <label for="floatingPassword">Type Password Again</label>
        <div class="error" v-if="v$.repeatPassword.$error">
          Passwords must be identical.
        </div>
      </div>
      <div class="form-floating mb-3">
        <select name="move-list" id="move-list" v-model="subject_id" class="form-control">
          <option v-for="subject in allsubjects" :key="subject.subject_id" :value="subject.subject_id">
            {{ subject.subject_name }}
          </option>
        </select>
        <label for="move_list">Choose your Subject</label>
        <div class="error" v-if="v$.subject_id.$error">
          Choose the subject to proceed
        </div>
      </div>
      <button class="w-100 btn btn-lg btn-primary" type="submit">
        Register
      </button>
      <p class="mt-5 mb-3 text-muted">&copy; SupportCentral</p>
    </form>
    <div class="text-center">
      Already a Staff/Student?
      <router-link class="link-primary" to="/"> Sign-in</router-link>
    </div>
  </main>
</template>

<script>
import router from "@/router";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength, sameAs, email } from "@vuelidate/validators";
export default {
  setup() {
    return {
      v$: useVuelidate(),
    };
  },
  name: "RegisterStaff",
  data: function () {
    return {
      username: "",
      password: "",
      errormsg: "",
      email: "",
      subject_id: "",
      repeatPassword: "",
      errStatus: false,
      allsubjects: [],
    };
  },
  validations() {
    return {
      username: { required },
      email: { required, email },
      password: { required, minLength: minLength(5) },
      repeatPassword: { sameAsPassword: sameAs(this.password) },
      subject_id: { required },
    };
  },
  methods: {
    handleFormRegister: function () {
      console.log("before touch");
      this.v$.$touch();
      if (this.v$.$error) {
        console.log("fail");
      } else {
        fetch("http://127.0.0.1:5500/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
            role: "staff",
            subject_id: this.subject_id,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              alert("Please use a different Email-ID");
            }
            return response.json();
          })
          .then((data) => {
            console.log(data);
            if (data.access_token) {
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("username", this.username);
              localStorage.setItem("role", "staff");
              localStorage.setItem("user_id", data.user_id);
              alert("Please wait for your approval")
              router.push("/");
            } else {
              this.errStatus = true;
              this.errormsg = data.error_message;
              this.username = null;
              this.password = null;
            }
          })
          .catch((err) => {
            console.log(err);
            this.errStatus = true;
            this.errormsg = "subject doesn't exist";
            this.username = null;
            this.password = null;
          });
      }
    },
  },
  mounted: function () {
    fetch(`http://127.0.0.1:5500/api/tag/subject`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    })
      .then((response) => {
        if (!response.ok) {
          alert("Response not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data) {
          this.allsubjects = data;
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style scoped>
.error {
  text-align: left;
  color: red;
}
</style>
