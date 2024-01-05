<script setup>
import { ref } from 'vue';
import axios from 'axios';

const info = ref('Nothing here yet!');
const fileInput = ref(null);

async function submitFile() {
    let formData = new FormData();
    formData.append('file', this.fileInput);
    console.log(this.file);

    await axios.post('http://127.0.0.1:8000/lang', formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((response) => {
            console.log('SUCCESS!!');
            info.value = response.data;
            console.log(info.value);
        }).catch(function () {
            console.log('FAILURE!!');
        });

}

function handleFileChange() {
    fileInput = fileInput.value.files[0];
}
</script>

<template>
    <div>
        <h1>File Upload</h1>
        <form>
            <div style={{ margin-bottom: 20 }}>
                <input type="file">
            </div>
            <button type="submit">Upload</button>
        </form>
    </div>
</template>