<script setup>
import { ref } from 'vue';

const info = ref(null);
const fileInput = ref(null);
let uploaded = ref(false);

const submitFile = async () => {
    const formData = new FormData();
    formData.append('file_upload', fileInput.value);

    const endpoint = 'http://127.0.0.1:8000/lang';

    try {
        const response = await fetch(endpoint, { method: 'POST', body: formData })
            .then((result) => result.json())
            .then((data) => {
                console.log('SUCCESS!!');
                console.log(data);
                info.value = data.lang;
                console.log(info.value);
                uploaded.value = true;
            })
            .catch((result) => {
                console.log('FAILURE!!');
                console.log(result);
            })
    } catch (e) {
        console.log(e);
    }

}

const handleFileChange = (event) => {
    fileInput.value = event.target.files[0];
}
</script>

<template>
    <div>
        <h1>Language Finder</h1>
        <form>
            <div class="upl_btn">
                <input type="file" id="fileInput" ref="fileInput" @change="handleFileChange($event)">
            </div>
            <button type="submit" @click.prevent="submitFile">Upload</button>
        </form>
        <p v-if="uploaded">The file is most likely written in {{ info }}</p>
        <p v-else> </p>
    </div>
</template>

<style>
.upl_btn {
    margin-bottom: 20px;
}
</style>