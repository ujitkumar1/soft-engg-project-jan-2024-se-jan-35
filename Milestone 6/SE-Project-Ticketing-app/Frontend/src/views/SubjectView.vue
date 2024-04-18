<template>
  <div>
    <NavBar :title="title"></NavBar>
    <SideBar @filter-change="tagFilter" @Reset="resetFilter" :reload="reload"></SideBar>
    <span class="btn-group btn-group-lg" style="margin-left: 20rem">
      <input type="radio" class="btn-check" value="faq" v-model="selectedOption" @change="FAQ" id="btnradio1" />
      <label class="btn btn-outline-primary" for="btnradio1">FAQ</label>

      <input type="radio" class="btn-check" value="resolved" v-model="selectedOption" @change="RESOLVED" id="btnradio2" />
      <label class="btn btn-outline-primary" for="btnradio2">Resolved</label>

      <input type="radio" class="btn-check" value="unresolved" v-model="selectedOption" @change="UNRESOLVED"
        id="btnradio3" />
      <label class="btn btn-outline-primary" for="btnradio3">Unresolved</label>
    </span>
    <div class="container pt-2">
      <div class="text-center" v-if="!filtered_list.length">
        <img src="../assets/notFound.jpg" alt="No image found">
        <h3>No tickets found under this section.</h3>
      </div>
      <div class="row m-1" v-for="ticket in filtered_list" :key="ticket.title">
        <div class="card position-relative" style="width: 84%; margin-left: 13rem; min-height: 4em">
          <div style="font-size: 2.5em" class="position-absolute">
            {{ ticket.likes }}
          </div>
          <div style="font-size: 1.5em; width: 90%; margin-left: 2.5em" class="mt-1">
            <div v-if="ticket.sec_name">
              <span class="badge bg-primary">{{ ticket.sec_name }}</span><br />
            </div>
            <router-link :to="'/ticket/' + ticket.ticket_id">{{ ticket.title }}</router-link>
          </div>
        </div>
      </div>
      <CreateTicket :subject_tag="subject_name" v-if="role == 'student'" />
    </div>
  </div>
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import SideBar from "@/components/SideBar.vue";
import router from "@/router";
import CreateTicket from "@/components/CreateTicket.vue";
export default {
  name: "SubjectView",
  components: {
    NavBar,
    CreateTicket,
    SideBar
  },
  data: function () {
    return {
      subject_name: this.$route.params.subject,
      title: this.$route.params.subject,
      ticket_list: [],
      filtered_list: [],
      search: "",
      selectedOption: "faq",
      reload: false,
      role: localStorage.getItem("role")
    };
  },
  methods: {
    tagFilter(value) {
      this.reload = false;
      this.filtered_list = this.ticket_list.filter(x => x.sec_name == value)
    },
    resetFilter() {
      this.filtered_list = this.ticket_list;
    },
    FAQ() {
      this.reload = true;
      fetch(`http://127.0.0.1:5500/api/subject/${this.subject_name}?FAQ=True`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        }
      })
        .then((response) => {
          if (!response.ok) {
            alert("PLease login first");
            router.push("/");
          }
          return response.json();
        })
        .then((data) => {
          this.ticket_list = data;
          this.filtered_list = data;
        })
        .catch((err) => console.log(err));
    },
    RESOLVED() {
      this.reload = true;
      fetch(
        `http://127.0.0.1:5500/api/subject/${this.subject_name}?ResolvedStatus=True`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          }
        }
      )
        .then(response => response.json())
        .then((data) => {
          this.ticket_list = data;
          this.filtered_list = data;
        })
        .catch((err) => console.log(err));
    },
    UNRESOLVED() {
      this.reload = true;
      fetch(
        `http://127.0.0.1:5500/api/subject/${this.subject_name}?ResolvedStatus=False`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          }
        }
      )
        .then(response => response.json())
        .then((data) => {
          this.ticket_list = data;
          this.filtered_list = data;
        })
        .catch((err) => console.log(err));
    },
  },


  beforeMount() {
    if (localStorage.getItem('access_token') == null) {
      alert("Login first");
      return router.push("/");
    }
    if (localStorage.getItem('role') == 'staff' && localStorage.getItem('subject_name') != this.subject_name) {
      alert("You are not authorised to change url and access other subject page")
      localStorage.clear()
      return router.push(`/`);


    }

    this.FAQ();
  },
};
</script>
<style scoped>
hr {
  border-top: solid #182825;
  border-width: 5px;
}

.card {
  background-color: #b8b4ff;
  color: #653239;
}


a {
  color: #653239;
  text-decoration: none;
}

form.search {
  display: inline-block;
  margin-left: 23%;
  width: auto;
}

input[type='text'].search {
  padding: 1rem;
  width: 25rem;
  height: 3rem;
  border-radius: 50px;
  margin-right: -50px;
}
</style>
