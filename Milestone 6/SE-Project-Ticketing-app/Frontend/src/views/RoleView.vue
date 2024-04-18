<template>
    <div>
        <NavBarAdmin></NavBarAdmin>
        <span class="btn-group" style="margin-left: 15%;">
            <input type="radio" class="btn-check" value="approved" v-model="selectedOption" @change="APPROVED"
                id="btnradio1" />
            <label class="btn btn-outline-primary" for="btnradio1">Approved</label>

            <input type="radio" class="btn-check" value="unapproved" v-model="selectedOption" @change="UNAPPROVED"
                id="btnradio2" />
            <label class="btn btn-outline-primary" for="btnradio2">UnApproved</label>
        </span>
        <form class="search" role="search">
            <input class="search" type="text" id="search" placeholder="Search Username here..." v-model="search"
                @input="search_function" />
            <button type="submit" class="btn btn-link"> <i class="bi bi-search"></i> </button>
        </form>
        <div class="container pt-2">
            <div class="text-center" v-if="!filtered_list.length">
                <img src="../assets/notFound.jpg" alt="No image found">
                <h3>No Staff data found under this section.</h3>
            </div>
            <div v-else>
                <div class="row m-1" v-for="(role, index) in filtered_list" :key="index">
                    <div class="card position-relative" style="width: 84%; left: 5rem; min-height: 4em">
                        <div style="font-size: 1.5em; width: 90%; margin-left: 2.5em" class="d-flex mt-1">
                            <div class="flex-grow-1 justify-content-start">
                                <ul>
                                    <li>Username: {{ role.username }} </li>
                                    <li>Email: {{ role.email }}</li>
                                    <li>Subject: {{ role.subject_name }}</li>
                                </ul>
                            </div>
                            <div class="align-self-center justify-content-end" v-if="selectedOption == 'approved'">
                                <EditRole :user_id="role.user_id"></EditRole>
                                <button class="btn btn-danger" @click="DelRole">Delete</button>
                            </div>
                            <div class="align-self-center justify-content-end" v-else>
                                <button class="btn btn-success me-2"
                                    @click="ApproveRole(role.user_id, role.subject_id)">Approve</button>
                                <button class="btn btn-danger" @click="DelRole(role.user_id)">Deny</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import NavBarAdmin from "@/components/NavBarAdmin.vue";
import EditRole from "@/components/EditRole.vue";
import router from "@/router";
// import EditTag from '@/components/EditTag.vue';

export default {
    name: "RoleView",
    components: {
        NavBarAdmin,
        EditRole,
    },
    data: function () {
        return {
            role_list: [],
            filtered_list: [],
            search: '',
            selectedOption: "approved",
            role: localStorage.getItem("role")
        };
    },
    methods: {
        search_function() {
            this.filtered_list = this.role_list.filter(x => x.username.toLowerCase().includes(this.search.toLowerCase()))
        },
        APPROVED() {
            fetch(`http://127.0.0.1:5500/api/role?status=1`, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                }
            })
                .then(response => response.json())
                .then((data) => {
                    this.role_list = data;
                    this.filtered_list = data;
                })
                .catch((err) => console.log(err));
        },
        UNAPPROVED() {
            fetch(`http://127.0.0.1:5500/api/role?status=0`, {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                }
            })
                .then(response => response.json())
                .then((data) => {
                    this.role_list = data;
                    this.filtered_list = data;
                })
                .catch((err) => console.log(err));
        },
        DelRole(user_id) {
            if (confirm('Are you sure you want to remove this?')) {
                fetch(`http://127.0.0.1:5500/api/role/${user_id}`, {
                    method: 'DELETE',
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    }
                }).catch((err) => console.log(err));
                this.role_list = this.role_list.filter(x => x.user_id != user_id)
                this.search_function()
            }
        },
        ApproveRole(user_id, subject_id) {
            if (confirm('Do you want to approve the staff?')) {
                fetch(`http://127.0.0.1:5500/api/role/${user_id}`, {
                    method: 'PUT',
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify({
                        subject_id: subject_id,
                        status: true
                    })
                })
                    .then(response => response.json())
                    .then((data) => {
                        if (data) {
                            window.location.reload();
                        }
                        else {
                            this.errStatus = true;
                            this.errormsg = data.error_message;
                        }
                    })
                    .catch((err) => {
                        console.log(err);
                        this.errStatus = true;
                        this.errormsg = "Invalid subject";
                    });
            }
        },
    },
    beforeMount() {
        if (localStorage.getItem('access_token') == null) {
            alert('Please Login First')
            return router.push('/')
        }
        this.APPROVED();
    },
}
</script>
<style scoped>
form.search {
    display: inline-block;
    margin-left: 24%;
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