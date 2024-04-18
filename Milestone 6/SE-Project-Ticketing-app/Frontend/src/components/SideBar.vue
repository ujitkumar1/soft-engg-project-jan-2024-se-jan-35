<template>
    <div class="mt-3">
        <div class="sidebar">
            <p class="mt-2 ms-3">Filter tickets by</p>
            <button style="margin-left: 75%; font-size: small;position: absolute;" @click="reset">Reset</button>
            <div class="form-check ms-3 pt-3 me-3">
                <div v-for="(tag, index) in sec_tag_list" :key="index">
                    <input class="form-check-input" type="radio" :value=tag :id=index v-model="selectedOption"
                        @change="notify">
                    <label class="form-check-label" :for=index>{{ tag }} </label>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "SideBar",
    data() {
        return {
            selectedOption: '',
            sec_tag_list: ''
        }
    },
    props: ["reload"],
    methods: {
        notify() {
            this.$emit('filter-change', this.selectedOption);
        },
        reset() {
            this.selectedOption = '';
            this.$emit('reset');
        }
    },
    watch: {
        reload(oldv) {
            if (oldv) {
                this.reset();
            }
        }
    },
    beforeCreate() {
        fetch(`http://127.0.0.1:5500/api/tag/secondary`)
            .then(res => res.json())
            .then((data) => {
                if (data) {
                    this.sec_tag_list = data.map(x => x.sec_name);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }
};
</script>
<style>
.sidebar {
    font-size: x-large;
    width: 15rem;
    min-height: 75%;
    background-color: #f2f2f2;
    left: 3%;
    position: absolute;
}

div.form-check {
    height: 80%;
    overflow-y: auto;
}
</style>