<template>
    <div>
        <i type="button" class="bi bi-plus-circle-fill text-success plus" style="font-size: 4rem" data-bs-toggle="modal"
        data-bs-target="#exampleModal">
        </i>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title text-danger" id="exampleModalLabel">
                            Create Tag Form
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="CreateTag">
                            <div v-if="errStatus">
                                <br />
                                <p class="alert alert-danger">{{ errormsg }}</p>
                            </div>
                            <div class="form-floating mb-3">
                                <input type="text" v-model="tag_name" class="form-control" id="floatingInput" placeholder="Tag Name" />
                                <label for="floatingInput">Tag Name</label>
                                <div class="error" v-if="v$.tag_name.$error">
                                Tag Name is required
                                </div>
                            </div>
                            <div class="form-check">
                                <select v-model= "TagType" class="form-select" aria-label="Default select example">
                                    <option v-for="option in this.options" :key="option.value" :value="option.value">{{ option.text }}</option>
                                </select>
                                <div class="error" v-if="v$.TagType.$error">
                                    Choose the tag type to proceed
                                </div>
                            </div>
                            <button class="w-100 btn btn-lg btn-block" type="submit">
                            Create Tag
                            </button>
                        </form>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-warning" data-bs-dismiss="modal">
                            Close
                            </button>
                        </div>
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
    name: "CreateTag",
    data : function(){
        return {
            tag_name: "",
            TagType: "subject",
            options: [
                {text: "Subject Tag", value: "subject"},
                {text: "Secondary Tag", value: "secondary"}
            ],

            errormsg: "",
            errStatus: false,
        };
    },
    validations(){
        return {
            tag_name: { required },
            TagType: { required },
        };
    },
    methods: {
        CreateTag: function(){
            this.v$.$touch();
            if(this.v$.$error){
                console.log("fail")
            }
            else {
                fetch(`http://127.0.0.1:5500/api/tag/${this.TagType}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify({
                        tag_name: this.tag_name
                    })
                })
                .then((response) => {
                    return response.json()
                })
                .then((data) => {
                    if (data){
                        window.location.reload();
                    }
                    else {
                        this.errStatus = true;
                        this.errormsg = data.error_message;
                        this.tag_name = null;
                    }
                })
                .catch((err) => {
                    console.log(err);
                    this.errStatus = true;
                    this.errormsg = "This Tag already exists";
                    this.tag_name = null
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