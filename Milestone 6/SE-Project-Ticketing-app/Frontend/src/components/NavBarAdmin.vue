<template>
    <nav class="navbar navbar-dark navbar-expand-lg shadow p-2 mb-5" style="background-color: #6f2cf3;">
        <div class="container-fluid">
            <router-link to="/tag" class="navbar-brand">
                <img src="../assets/logo1_small.png" alt="Logo" width="50" height="50" class="d-inline-block align-text">
                Support Central
            </router-link>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <router-link to="/tag" class="nav-link" aria-current="page">Tags</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/role" class="nav-link" aria-current="page">Roles</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/dash" class="nav-link" aria-current="page">Subjects</router-link>
                    </li>
                </ul>
            </div>
            <div class="position-absolute top-0 end-0 mt-3 me-3 collapse navbar-collapse">
                <button @click="logout" style="font-size: large; color: whitesmoke" class="btn btn-danger">
                    Logout <i class="bi bi-box-arrow-right"></i>
                </button>
            </div>
        </div>
    </nav>
</template>
<script>
import router from "@/router";
export default {
    name: "NavBarAdmin",
    data() {
        return {
            role: localStorage.getItem("role")
        }
    },
    methods: {
        logout() {
            localStorage.clear();
            return router.push("/");
        }
    },
}
</script>
<style scoped></style>