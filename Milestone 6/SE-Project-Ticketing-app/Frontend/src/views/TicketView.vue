<template>
  <NavBar :title="ticket_details.subject_name" isSubject="true"></NavBar>
  <div class="container-fluid mt-1" style="width: 70%; margin: auto">

    <!-- Question Card -->
    <div class="d-flex">
      <div class="card" style="min-height: 4em; width: 100%;">
        <div class="card-header" :class="{
          'bg-success': ticket_details.ticket_status == 'resolved',
          'bg-danger': ticket_details.ticket_status == 'unresolved',
        }">
          <h5>Question</h5>
        </div>
        <div class="row">
          <div class="col-1 d-flex flex-column align-items-center justify-content-center">
            <i @click="like(ticket_details.ticket_id)" :class="[
              'bi', isLiked ? 'bi-hand-thumbs-up-fill txt-color' : 'bi-hand-thumbs-up',
            ]" style="font-size: 2rem" data-toggle="tooltip" data-placement="top" title="Like"></i>
            <p>{{ likes }}</p>
          </div>
          <div class="col">
            <div class="card-body">
              <h5 class="card-title">{{ ticket_details.title }}</h5>
              <p class="card-text">{{ ticket_details.description }}</p>
              <div class="card-footer text-body-secondary">
                Tags:
                <div class="badge txt-button">
                  {{ ticket_details.sec_name }}
                </div>
                <div class="badge txt-button">
                  {{ ticket_details.ticket_status }}
                </div>

        <button class="btn btn-primary m-3" @click="ticketflag(ticket_details.ticket_id,ticket_details.title)">Flag</button>
                <div v-if="ticket_details.isFAQ" class="badge txt-button">
                  FAQ
                </div>
                <div v-if="duplicate" class="badge bg-danger">
                  Duplicate
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="role == 'admin'" class="d-flex ms-2 align-items-center justify-content-center"><i
          @click="Delete(ticket_details.ticket_id)" class="bi bi-trash-fill text-danger" style="font-size: 2rem"
          data-toggle="tooltip" data-placement="top" title="Delete"></i></div>

    </div>

    <div class="d-flex justify-content-end">
      <div v-if="!this.duplicate && this.role != 'student'">
        <button v-if="!ticket_details.isFAQ" class="btn btn-primary m-3" @click="MarkFAQ(ticket_details.ticket_id)">Mark
          FAQ</button>
        <button v-if="ticket_details.isFAQ" class="btn btn-danger m-3" @click="UnMarkFAQ(ticket_details.ticket_id)">UnMark
          FAQ</button>
      </div>

      <button v-if="!duplicate && this.role != 'student'" class="btn btn-danger m-3"
        @click="MarkDuplicate(ticket_details.ticket_id)">Mark Duplicate</button>
    </div>


    <!-- Solution Card -->

    <div v-if="ticket_details.ticket_status == 'resolved'" class="card m-3" style="min-height: 4em">
      <div class="card-header bg-success">
        <h5>Solution</h5>
      </div>
      <div class="row">

        <div class="col">
          <div class="card-body">
            <p class="card-text">{{ true_response }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Responses Card -->
    <hr class="border border-success border-2 opacity-100" />
    <h2>Responses</h2>
    <div class="row p-3" v-for="response in response_list" :key="response.id">
      <div class="card" :class="{ 'border-success': response.isAnswer }" style="min-height: 4em">
        <div class="row">
          <div class="col">

            <div class="card-body">
              <p class="card-title">{{ response.response }}</p>
              <div v-if="ticket_details.user_id == current_user_id || role == 'admin'">
                <div class="d-flex justify-content-end">
                  <p class="card-text me-2" :class="{ 'h5 text-success': response.isAnswer }">
                    Solution</p>
                  <i @click="MarkAnswer(ticket_details.ticket_id, response.response_id)"
                    :class="['bi', response.isAnswer == true ? 'bi-check-circle-fill text-success' : 'bi-check-circle',]"
                    style="font-size: 1.2rem" data-toggle="tooltip" data-placement="top" title="Solution"></i>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <div class="d-flex justify-content-end"><span class="text-secondary">Posted by: </span>
                {{ response.username }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row m-3">

      <!-- Response Form -->
      <form v-if="ticket_details.ticket_status == 'unresolved'" @submit.prevent="AddResponse">
        <div class="form-floating mb-3">
          <textarea type="textarea" v-model="response_text" class="form-control" id="floatingContent"
            placeholder="Please enter your Content" style="min-height: 8em" />
          <label for="floatingContent">Type your Response here</label>
        </div>

        <div class="d-flex justify-content-center">
          <button class="btn txt-button" style="color:whitesmoke" type="submit">Add Response</button>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import router from '@/router';

export default {

  name: "TicketView",
  components: { NavBar },
  data: function () {
    return {
      current_user_id: parseInt(localStorage.getItem("user_id")),
      username: "",
      response_text: "",
      ticket_details: {},
      response_list: [],
      likes: 0,
      isLiked: false,
      true_response: "",
      duplicate: false,
      role: "student"
    };
  },

  methods: {
    AddResponse() {
      if (!this.response_text.trimStart()) {
        alert("Empty response body is not allowed.")
      }
      else {
        fetch(`http://127.0.0.1:5500/api/response/${this.$route.params.id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            user_id: localStorage.getItem("user_id"),
            response: this.response_text.trimStart(),
          }),
        })
          .then((response) => {
            if (!response.ok) {
              alert("Error occured while adding response");
            }
            return response.json();
          })
          .then((data) => {
            console.log(data);
            if (data) {
              // Send Notification to the ticket author abt new response
              fetch(`http://127.0.0.1:5500/notify/student`, {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "*",
                  Authorization: "Bearer " + localStorage.getItem("access_token"),
                },
                body: JSON.stringify({
                  username: this.username,
                  ticket_id: this.$route.params.id,
                })
              })
              window.location.reload();
            } else {
              this.response_text = null;
            }
          })
          .catch((err) => {
            console.log(err);
            this.response_text = null;
          });
      }
    },
    like(id) {
      this.isLiked ? (this.likes -= 1) : (this.likes += 1),
        (this.isLiked = !this.isLiked);
      fetch(`http://127.0.0.1:5500/api/subject/ticket/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          action: "like",
          user_id: parseInt(this.current_user_id),
        }),
      })
        .then((response) => {
          if (!response.ok) {
            alert("Error occured while liking this ticket");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
        })
        .catch((err) => console.log(err));
    },
    Delete(id) {

      fetch(`http://127.0.0.1:5500/api/subject/ticket/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            alert("Error occured while deleting this ticket");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          router.push(`/subject/${this.ticket_details.subject_name}`)
        })
        .catch((err) => console.log(err));
    },

    ticketflag(ticket_id,title){
               fetch(`http://127.0.0.1:5500/flag_post`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          ticket_id: ticket_id,
          ticket_name: title,
        }),
      })
        .then((response) => {
          if (!response.status) {
            alert("Error occurred while flagging the post ");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data); })
          },


    MarkAnswer(ticket_id, res_id) {
      fetch(`http://127.0.0.1:5500/api/response/${ticket_id}/${res_id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          isAnswer: true,
          ticket_status: "resolved",
        }),
      })
        .then((response) => {
          if (!response.ok) {
            alert("Error occurred while marking response as answer");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);

          this.ticket_details.ticket_status = "resolved";

          for (let response of this.response_list) {
            if (response.response_id == res_id) {
              response.isAnswer = true;
              this.true_response = response.response
            } else {
              response.isAnswer = false;
            }
          }

          console.log(this.response_list);
        })
        .catch((err) => console.log(err));
    },
    MarkFAQ(id) {
      fetch(`http://127.0.0.1:5500/api/subject/ticket/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          action: "faq",
          user_id: parseInt(this.current_user_id),
        }),
      })
        .then((response) => {

          return response.json();
        }
        )
        .then((data) => {
          if (data.error_code) {
            alert(data.error_message)
          }
          else {
            this.ticket_details.isFAQ = true
          }

        })
        .catch((err) => console.log(err));
    },
    UnMarkFAQ(id) {
      fetch(`http://127.0.0.1:5500/api/subject/ticket/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          action: "notfaq",
          user_id: parseInt(this.current_user_id),
        }),
      })
        .then((response) => {

          return response.json();
        }
        )
        .then((data) => {
          if (data.error_code) {
            alert(data.error_message)
          }
          else {
            this.ticket_details.isFAQ = false
          }
        })
        .catch((err) => console.log(err));
    },
    MarkDuplicate(id) {
      let title = prompt("Please input the url of original ticket");
      if (title) {
        fetch(`http://127.0.0.1:5500/api/response/${id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            user_id: localStorage.getItem("user_id"),
            response: "Duplicate ticket, Original thread link: " + title,
          }),
        })
          .then(response => response.json())
          .then((data) => {
            if (data.error_code) {
              alert(data.error_message)
            }
            else {
              this.duplicate = true
              this.response_list = data.response_list
              const index = this.response_list.findIndex(item => item.response.includes('Duplicate ticket'));
              const res_id = parseInt(this.response_list[index].response_id)
              fetch(`http://127.0.0.1:5500/api/response/${this.ticket_details.ticket_id}/${res_id}`, {
                method: "PUT",
                headers: {
                  "Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "*",
                  Authorization: "Bearer " + localStorage.getItem("access_token"),
                },
                body: JSON.stringify({
                  isAnswer: true,
                  ticket_status: "resolved",
                }),
              })
                .then((response) => {
                  if (!response.ok) {
                    alert("Error occurred while marking as duplicate");
                  }
                  return response.json();
                })
                .then((data) => {
                  console.log(data);
                  window.location.reload()
                })
                .catch((err) => console.log(err));
            }
          })
          .catch((err) => console.log(err));
      }
    },
  },
  beforeMount: function () {
    if (localStorage.getItem('access_token') == null) {
      alert('Please Login First.')
      return router.push('/')
    }
    this.username = localStorage.getItem("username");
    this.role = localStorage.getItem("role")
    fetch(`http://127.0.0.1:5500/api/response/${this.$route.params.id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    })
      .then((response) => {
        if (!response.ok) {
          alert("Error occurred while retrieving data.");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);

        if (this.role == 'staff') {
          if (data.subject_name !== localStorage.getItem("subject_name")) {
            alert("You are accessing other subject ticket")
            router.push(`/subject/${localStorage.getItem("subject_name")}`)
          }
        }
        this.ticket_details = data;
        this.response_list = data.response_list;
        this.likes = this.ticket_details.likes.length;
        this.isLiked = this.ticket_details.likes.includes(this.current_user_id);
        const answer = this.response_list[this.response_list.findIndex(
          (response) => response.isAnswer == true
        )];
        const index = this.response_list.findIndex(item => item.response.includes('Duplicate ticket'));
        if (index != -1) {
          this.duplicate = true
        }

        this.true_response = answer.response
      })
      .catch((err) => console.log(err));
  },
};
</script>
<style scoped>
.txt-button {
  background-color: #6b62ff;
}

.txt-color {
  color: #6b62ff;
}
</style>