<template>
  <div>
    <div v-if="!uploadComplete">
      <input type="file" ref="fileInput" @change="handleFileChange" multiple />
      <button @click="uploadFiles">Upload</button>
    </div>

    <div v-else>
      <p>Upload complete! <a :href="downloadLink" download>Click here to download the zip file</a></p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFiles: [],
      uploadComplete: false,
      downloadLink: "",
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFiles = Array.from(event.target.files);
    },
    async uploadFiles() {
      const formData = new FormData();
      this.selectedFiles.forEach((file) => {
        formData.append("files", file);
      });

      try {
        const response = await axios.post("http://localhost:8000/upload/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        this.uploadComplete = true;
        this.downloadLink = response.data.download_link;
      } catch (error) {
        console.error("Error uploading files:", error);
      }
    },
  },
};
</script>
