<template>
    <div>
        <NavBar :title="title" :isSearch="false"></NavBar>
        <div>
            <SideBar @filter-change="tagFilter" @Reset="resetFilter" :reload="reload"></SideBar>
            <form class="search" @submit.prevent="search_function">
                <input class="search" type="text" id="search" placeholder="Search here...." v-model="search" />
                <button type="submit" class="btn btn-link"> <i class="bi bi-search"></i> </button>
            </form>
            <div class="container pt-2">
                <div class="row">
                    <div class="text-center" v-if="!filtered_list.length">
                        <img src="../assets/notFound.jpg" alt="No image Found" sizes="" srcset="">
                        <h3>No tickets found under this section.</h3>
                    </div>
                    <div class="row m-1" v-for="ticket in filtered_list" :key="ticket.title">
                        <div class="card position-relative">
                            <div style="font-size: 2.5em" class="position-absolute">
                                {{ ticket.likes }}
                            </div>
                            <div style="font-size: 1.5em; width: 90%; margin-left: 2.5em" class="mt-1">
                                <span class="badge bg-success me-2" v-if="ticket.ticket_status == 'resolved'">
                                    Resolved
                                </span>
                                <span class="badge bg-secondary me-2" v-else> Unresolved</span>

                                <span class="badge bg-info me-2">{{ ticket.subject_name }}</span>
                                <span class="badge bg-primary">{{ ticket.sec_name }}</span><br>
                                <router-link :to="'/ticket/' + ticket.ticket_id">{{ ticket.title }}</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import NavBar from "@/components/NavBar.vue";
import SideBar from "@/components/SideBar.vue";
import router from "@/router";
export default {
    name: 'SeacrhComp',
    components: {
        NavBar,
        SideBar
    },
    data() {
        return {
            title: "Search Page",
            ticket_list: [],
            filtered_list: [],
            search: this.$route.params.search,
            reload: false,
            subject_name: localStorage.getItem("subject_name"),
            role: localStorage.getItem("role")
        }
    },
    methods: {
        search_function() {
            this.reload = true;
            this.ticket_list = [];
            this.filtered_list = []
            if (this.role == 'staff') {
                fetch(`http://127.0.0.1:5500/api/subject/${this.subject_name}?search=${this.search}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    }
                })
                    .then(res => res.json())
                    .then((data) => {
                        this.ticket_list = data;
                        this.filtered_list = data;
                    })
                    .catch((err) => console.log(err));
            } else {
                fetch(`http://127.0.0.1:5500/api/tag/subject`)
                    .then(res => res.json())
                    .then(data => {
                        const subjects = data.map(x => x.subject_name)
                        //Format-> ['BDM', 'BA', 'MLT', 'AppDev-1', 'AppDev-2']
                        subjects.forEach(name => {
                            fetch(`http://127.0.0.1:5500/api/subject/${name}?search=${this.search}`, {
                                method: "GET",
                                headers: {
                                    "Content-Type": "application/json",
                                    "Access-Control-Allow-Origin": "*",
                                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                                }
                            })
                                .then(res => res.json())
                                .then((data) => {
                                    if (data.length) {
                                        this.ticket_list.push(...data);
                                        this.filtered_list.push(...data);
                                    }
                                })
                                .catch((err) => console.log(err));
                        });
                    })
            }
        },
        tagFilter(value) {
            this.reload = false;
            this.filtered_list = this.ticket_list.filter(x => x.sec_name == value)
        },
        resetFilter() {
            this.filtered_list = this.ticket_list;
        },
    },
    beforeMount() {
        if (localStorage.getItem('access_token') == null) {
            alert('Please Login First.')
            return router.push('/')
        }
        this.search_function();
    },
}
</script>
<style scoped>
form.search {
    display: inline-block;
    margin-left: 25%;
    width: auto;
}

input[type='text'].search {
    padding: 1rem;
    width: 35rem;
    height: 3rem;
    border-radius: 50px;
    margin-right: -50px;
}

.card {
    width: 65%;
    margin: auto;
    min-height: 4em;
    /* background-color: #b8b4ff; */
    color: #000;
    /* color: #653239; */
}

a {
    /* color: #653239; */
    color: black;
    text-decoration: none;
}
</style>