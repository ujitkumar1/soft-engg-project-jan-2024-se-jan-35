<template>
    <div>
        <div v-if="!editing">
            <label>{{ label }}</label>

            <i @click="editing = true, newLabel = label" class="bi bi-pencil text-primary h5 mx-2" data-toggle="tooltip"
                data-placement="top" title="Edit"></i>
        </div>
        <div v-else>
            <input type="text" class="no-border" v-model="newLabel">
            <i @click="saveNewLabel" class="bi bi-check-lg text-success h5" data-toggle="tooltip" style="font-size: 2rem"
                data-placement="top" title="Save"></i>

            <i @click="editing = false" class="bi bi-x text-danger h5" data-toggle="tooltip" style="font-size: 2rem"
                data-placement="top" title="Save"></i>
        </div>
    </div>
</template>
<script>


export default {
    name: "EditTag",
    data: function () {
        return {
            tag_name: "",
            errormsg: "",
            errStatus: false,
            newLabel: '',
            editing: false
        };
    },
    props: ["tag_id", "TagType", "label"],

    methods: {
        saveNewLabel() {
            console.log(this.newLabel)
            if (this.newLabel !== '') {
                fetch(`http://127.0.0.1:5500/api/tag/${this.TagType}/${this.tag_id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token"),
                    },
                    body: JSON.stringify({
                        tag_name: this.newLabel
                    })
                })
                    .then((response) => {
                        return response.json()
                    })
                    .then((data) => {
                        if (data) {
                            console.log(data)
                        }
                        else {
                            this.errStatus = true;
                            this.errormsg = data.error_message;
                            this.tag_name = null;
                        }
                    })
                    .catch((err) => {
                        console.log(err);
                        alert("This tag already exists")
                        this.errStatus = true;
                        this.errormsg = "This Tag already exists";
                        this.tag_name = null
                    });
                this.$emit('update-label', this.newLabel, this.TagType, this.tag_id);
                this.editing = false;
                this.newLabel = '';
            }
        },
    },
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