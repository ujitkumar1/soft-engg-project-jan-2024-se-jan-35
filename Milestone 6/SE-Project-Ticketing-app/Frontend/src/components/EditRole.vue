<template>
    <div>
        <button class="btn btn-block" data-bs-toggle="modal" :data-bs-target="'#' + user_id">Edit</button>
        <div class="modal fade" :id="user_id" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title text-danger" id="exampleModalLabel">
                            Edit Role Form
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="editRole">
                            <div v-if="errStatus">
                                <br />
                                <p class="alert alert-danger">{{ errormsg }}</p>
                            </div>
                            <div class="form-check">
                                <select v-model="subject_id" class="form-select" aria-label="Default select example"
                                    required>
                                    <option v-for="subject in subject_list" :key="subject.subject_name"
                                        :value="subject.subject_id">
                                        {{ subject.subject_name }}
                                    </option>
                                </select>
                                <div class="error" v-if="v$.subject_id.$error">
                                    Choose the subject to proceed
                                </div>
                            </div>
                            <button class="w-100 btn btn-lg btn-block" type="submit">
                                Submit
                            </button>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-warning" data-bs-dismiss="modal">
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { useVuelidate } from "@vuelidate/core";
import { required } from "@vuelidate/validators";

export default {
    setup() {
        return {
            v$: useVuelidate(),
        };
    },
    name: "EditRole",
    data: function () {
        return {
            title: this.user_id,
            subject_id: "",
            subject_list: [],
            errormsg: "",
            errStatus: false,
        };
    },
    props: ['user_id'],
    validations() {
        return {
            subject_id: { required },
        };
    },
    methods: {
        editRole() {
            this.v$.$touch();
            if (this.v$.$error) {
                console.log("fail")
            }
            else {
                fetch(`http://127.0.0.1:5500/api/role/${this.user_id}`, {
                    method: 'PUT',
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify({
                        subject_id: this.subject_id,
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
                            this.subject_id = null;
                        }
                    })
                    .catch((err) => {
                        console.log(err);
                        this.errStatus = true;
                        this.errormsg = "Invalid subject";
                        this.subject_id = null
                    });
            }
        }
    },
    // },
    created() {
        fetch(`http://127.0.0.1:5500/api/tag/subject`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        })
            .then(response => response.json())
            .then((data) => {
                if (data) {
                    this.subject_list = data;
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }
};
</script>
<style scoped>
.btn-block {
    background-color: rgb(107, 98, 255);
}

.error {
    text-align: left;
    color: red;
}
</style>