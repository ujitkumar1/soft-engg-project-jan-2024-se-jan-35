<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <div class="navbar-brand mx-auto">
        <router-link to="/">
          <img src="../assets/logo1.png" alt="Logo" width="180" height="80" class="d-inline-block align-text-top" />
        </router-link>
      </div>

      <router-link to="/enroll">
        <div class="txt-color">Enroll as Staff</div>
      </router-link>
    </div>
  </nav>

  <div class="home">
    <div class="content">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <img src="../assets/undraw_remotely_2j6y.svg" alt="Image" class="img-fluid" />
          </div>
          <div class="col-md-6 contents">
            <div class="row justify-content-center">
              <div class="col-md-8">
                <div class="mb-4">
                  <h3 class="txt-color">Sign In</h3>
                  <p>Common sign-in destination for all</p>
                </div>
                <form @submit.prevent="handleFormSubmit">
                  <div v-if="errStatus">
                    <br />
                    <p class="alert alert-danger">{{ errormsg }}</p>
                  </div>
                  <div class="form-floating mb-3">
                    <input type="text" v-model="username" class="form-control" id="floatingInput"
                      placeholder="username" />
                    <label for="floatingInput">Username</label>
                    <div class="error" v-if="v$.username.$error">
                      Username is required.
                    </div>
                  </div>

                  <div class="form-floating mb-3">
                    <input type="password" v-model="password" class="form-control" id="floatingPassword"
                      placeholder="Password" />
                    <label for="floatingPassword">Password</label>
                    <div class="error" v-if="v$.password.$error">
                      Password is required and must be of minimum 5 characters.
                    </div>
                  </div>

                  <input type="submit" value="Log In" class="w-100 btn btn-block btn-primary" />
                </form>

                <div class="mt-3 text-left fw-bold">
                  New Student?
                  <router-link class="link-primary" to="/register">Register</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="typewriter">
      <h4 class="txt-color">
        Helping you achieve success,
        <span style="background-color: #6b62ff; color: whitesmoke">one ticket</span>
        at a time.
      </h4>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import router from "@/router";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength } from "@vuelidate/validators";

export default {
  setup() {
    return {
      v$: useVuelidate(),
    };
  },

  name: "HomeView",

  data: function () {
    return {
      username: "",
      password: "",
      errormsg: "",
      errStatus: false,
    };
  },
  validations() {
    return {
      username: { required },
      password: { required, minLength: minLength(5) },
    };
  },

  components: {},

  methods: {
    handleFormSubmit: function () {
      this.v$.$touch();
      if (this.v$.$error) {
        console.log("fail");
      } else {
        fetch("http://127.0.0.1:5500/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        })
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            console.log(data);
            if (data.access_token) {
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("username", this.username);
              localStorage.setItem("role", data.role);
              localStorage.setItem("user_id", data.user_id);
              if (data.role == 'staff') {
                localStorage.setItem("subject_name", data.subject_name)
                return router.push(`/subject/${data.subject_name}`)
              }
              else if (data.role == 'admin') {
                return router.push(`/tag`)
              }
              else { return router.push("/dash"); }

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
            this.errormsg = "This user doesn't exist";
            this.username = null;
            this.password = null;
          });
      }
    },
  },
};
</script>
<style scoped>
.btn-block {
  background-color: rgb(107, 98, 255);
}

.txt-color {
  color: #6b62ff;
}

.error {
  text-align: left;
  color: red;
}

body {
  background: #333;
  color: #fff;
  font-family: monospace;
  padding-top: 5em;
  display: flex;
  justify-content: center;
}

/* DEMO-SPECIFIC STYLES */
.typewriter h4 {
  text-align: center;

  overflow: hidden;
  /* Ensures the content is not revealed until the animation */
  border-right: 0.15em solid orange;
  /* The typwriter cursor */
  white-space: nowrap;
  /* Keeps the content on a single line */
  margin: 0 auto;
  /* Gives that scrolling effect as the typing happens */
  letter-spacing: 0.15em;
  /* Adjust as needed */
  animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
}

body {
  background: #333;
  color: #fff;
  font-family: monospace;
  padding-top: 5em;
  display: flex;
  justify-content: center;
}

/* The typing effect */
@keyframes typing {
  from {
    width: 0;
  }

  to {
    width: 70%;
  }
}

/* The typewriter cursor effect */
@keyframes blink-caret {

  from,
  to {
    border-color: transparent;
  }

  100% {
    border-color: blue;
  }
}
</style>
