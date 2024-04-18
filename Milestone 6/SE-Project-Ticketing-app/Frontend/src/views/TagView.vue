<template>
  <div>
    <NavBarAdmin></NavBarAdmin>
    <CreateTag></CreateTag>
    <span class="btn-group" style="margin-left: 9%;">
      <input type="radio" class="btn-check" value="subject_tags" v-model="selectedOption" @change="SUBJECTS"
        id="btnradio1" />
      <label class="btn btn-outline-primary" for="btnradio1">Subject Tags</label>

      <input type="radio" class="btn-check" value="secondary_tags" v-model="selectedOption" @change="SECONDARY"
        id="btnradio2" />
      <label class="btn btn-outline-primary" for="btnradio2">Secondary Tags</label>
    </span>
    <form class="search" role="search">
      <input class="search" type="text" id="search" placeholder="Search Tag name here..." v-model="search"
        @input="search_function" />
      <button type="submit" class="btn btn-link"> <i class="bi bi-search"></i> </button>
    </form>
    <div class="container pt-2">
      <div class="text-center" v-if="!filtered_list.length">
        <img src="../assets/notFound.jpg" alt="No image found">
        <h3>No tags found under this section.</h3>
      </div>
      <div v-else>
        <div v-if="selectedOption == 'subject_tags'">
          <div class="row m-3" v-for="tag in filtered_list" :key="tag.subject_id">
            <div class="card position-relative" style="min-height: 4em; width: 50%;">
              <div style="font-size: 1.5em; width: 90%; margin-left: 2.5em" class="d-flex mt-1">
                <EditTag :label="tag.subject_name" :tag_id="tag.subject_id" TagType="subject"
                  @update-label="updateLabel" />
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <div class="row m-3" v-for="tag in filtered_list" :key="tag.sec_id">
            <div class="card position-relative" style="min-height: 4em; width: 50%;">
              <div style="font-size: 1.5em; width: 90%; margin-left: 2.5em" class="d-flex justify-content-between mt-1">

                <EditTag :label="tag.sec_name" :tag_id="tag.sec_id" TagType="secondary" @update-label="updateLabel" />
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
import CreateTag from "@/components/CreateTag.vue";
import EditTag from "@/components/EditTag.vue"
import router from "@/router";

export default {
  name: "TagView",
  components: {
    NavBarAdmin,
    CreateTag,
    EditTag

  },
  data: function () {
    return {
      subject: "subject",
      secondary: "secondary",
      search: '',
      tag_list: [],
      filtered_list: [],
      selectedOption: "subject_tags",
      role: localStorage.getItem("role"),
      SubTagFlag: false,
      SecTagFlag: false

    };
  },
  methods: {
    search_function() {
      if (this.selectedOption == 'subject_tags') {
        this.filtered_list = this.tag_list.filter(x => x.subject_name.toLowerCase().includes(this.search.toLowerCase()))
      } else {
        this.filtered_list = this.tag_list.filter(x => x.sec_name.toLowerCase().includes(this.search.toLowerCase()))
      }
    },
    updateLabel(label, tagType, tag_id) {
      if (tagType == 'secondary') {
        this.tag_list.forEach(function (list) {
          if (list.sec_id === tag_id) {
            list.sec_name = label;
          }
        });
      }
      else {
        this.tag_list.forEach(function (list) {
          if (list.subject_id === tag_id) {
            list.subject_name = label;
          }
        });
      }
    },
    SUBJECTS() {
      fetch(`http://127.0.0.1:5500/api/tag/subject`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        }
      })
        .then((response) => {
          if (!response.ok) {
            alert("Please login first");
            router.push("/");
          }
          return response.json();
        })
        .then((data) => {
          this.tag_list = data;
          this.filtered_list = data;
        })
        .catch((err) => console.log(err));
    },
    SECONDARY() {
      fetch(`http://127.0.0.1:5500/api/tag/secondary`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        }
      })
        .then(response => response.json())
        .then((data) => {
          this.tag_list = data;
          this.filtered_list = data;
        })
        .catch((err) => console.log(err));
    },
  },

  beforeMount() {
    this.SUBJECTS();
  }
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
  width: 40rem;
  height: 3.2rem;
  border-radius: 50px;
  margin-right: -50px;
}
</style>