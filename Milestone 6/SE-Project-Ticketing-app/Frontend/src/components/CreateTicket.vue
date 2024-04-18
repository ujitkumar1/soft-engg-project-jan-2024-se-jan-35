<template>
  <div class="">
    <!-- Button trigger modal -->
    <i type="button" class="bi bi-plus-circle-fill text-success plus" style="font-size: 4rem" data-bs-toggle="modal"
      data-bs-target="#exampleModal">
    </i>

    <!-- Modal -->

    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-danger" id="exampleModalLabel">
              Create Ticket Form
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="CreateTicket">
              <!-- <img class="mb-4" src="../assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->
              <div v-if="errStatus">
                <br />
                <p class="alert alert-danger">{{ errormsg }}</p>
              </div>
              <h1 class="h3 mb-3 fw-normal">
                Create a new ticket in
                <span style="background-color: #6b62ff; color: whitesmoke">{{ subject_tag }}</span>
              </h1>

              <div class="form-floating mb-3">
                <input type="text" v-model="title" class="form-control" id="floatingInput" placeholder="Title" />
                <label for="floatingInput">Title</label>
                <div class="error" v-if="v$.title.$error">
                  Title is required
                </div>
              </div>

              <div class="form-floating mb-3">
                <textarea type="textarea" v-model="desc" rows="10" class="form-control" id="floatingContent"
                  placeholder="Please enter your Description" />
                <label for="floatingContent">Content</label>
                <div class="error" v-if="v$.desc.$error">
                  Content is required.
                </div>
              </div>
              <div class="form-floating mb-3">
                <select name="move-list" id="move-list" v-model="sec_tag_name" class="form-control">
                  <option v-for="sec_tag in sec_tag_list" :key="sec_tag.sec_id" :value="sec_tag.sec_name">
                    {{ sec_tag.sec_name }}
                  </option>
                </select>
                <label for="move_list">Choose your tag</label>
                <div class="error" v-if="v$.sec_tag_name.$error">
                  Choose the secondary tag to proceed
                </div>
              </div>

              <button class="w-100 btn btn-lg btn-block" type="submit">
                Create Ticket
              </button>
                    <label for="priority">Priority:</label>
    <select v-model="selectedPriority" id="priority" name="priority">
      <option value="normal">Normal</option>
      <option value="moderate">Moderate</option>
      <option value="urgent">Urgent</option>
    </select>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button"   class="btn btn-warning" data-bs-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
// import router from "@/router";
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";

export default {
  setup() {
    return {
      v$: useVuelidate(),
    };
  },
  name: "CreateTicket",
  data: function () {
    return {
      title: "",
      desc: "",
      sec_tag_name: "",
      sec_tag_list: [],

      errormsg: "",
      errStatus: false,
    };
  },
  props: ["subject_tag"],
  validations() {
    return {
      title: { required },
      desc: { required },
      sec_tag_name: { required }
    };
  },
  methods: {
    CreateTicket: function () {
      this.v$.$touch();
      if (this.v$.$error) {
        console.log("fail");
      } else {
        fetch(`http://127.0.0.1:5500/api/subject/${this.subject_tag}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            title: this.title,
            description: this.desc,
            secondary_tag: this.sec_tag_name,
            priority: this.selectedPriority

          }),
        })
          .then(response => response.json())
          .then((data) => {
            console.log(data);
            if (data) {
              // Send Notification to the staff abt new ticket
              fetch(`http://127.0.0.1:5500/notify/staff`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "*",
                  Authorization: "Bearer " + localStorage.getItem("access_token"),
                },
                body: JSON.stringify({
                  subject_name: this.subject_tag,
                  ticket_id: data.ticket_id
                })
              })
              window.location.reload();
            } else {
              this.errStatus = true;
              this.errormsg = data.error_message;
              this.title = null;
              this.desc = null;
            }
          })
          .catch((err) => {
            console.log(err);
            this.errStatus = true;
            this.errormsg = "This title already exists";
            this.title = null;
            this.desc = null;
          });
      }
    },
  },
  mounted: function () {
    fetch(`http://127.0.0.1:5500/api/tag/secondary`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        // Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    })
      .then((res1) => {
        return res1.json();
      })
      .then((data1) => {
        if (data1) {
          this.sec_tag_list = data1;
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>
<style scoped>
.btn-block {
  background-color: rgb(107, 98, 255);
}

.plus {
  position: fixed;
  bottom: 5%;
  right: 2%;
}

.error {
  text-align: left;
  color: red;
}
</style>
