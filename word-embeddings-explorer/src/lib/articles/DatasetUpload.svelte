<script>
    import axios from "axios";
    import { closeModal } from "svelte-modals";

    export let isOpen;
    export let loadDatasets;
    export let selectDataset;

    let files;
    let template;
    $: disabled = files === undefined || template === null;

    function loadDatasetTemplates()
    {
        let url = "http://127.0.0.1:5000/dataset-templates";
        let promise = axios.get(url);
        promise.then(response => { template = response.data[0]; });
        return promise;
    }

    function upload()
    {
        let url = "http://127.0.0.1:5000/dataset";
        let data = new FormData();
        data.append("dataset", files[0])
        let config = {
            params: {
                template,
                id: files[0].name,
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            }
        };
        axios.post(url, data, config)
             .then(loadDatasets)
             .then(() => { selectDataset(files[0].name); });
        closeModal();
    }
</script>

{#if isOpen}
    <div class="fixed inset-0 flex justify-center items-center pointer-events-none">
        <div class="p-8 w-1/3 rounded-md bg-white flex flex-col pointer-events-auto justify-between gap-2">
            <div class="pb-2 text-2xl border-b-2 border-sky-800">
                Upload your dataset
            </div>
            <div class="flex justify-between items-center">
                <p class="h-fit text-xl">
                    Dataset
                </p>
                <label for="file" class="p-2 w-fit border border-sky-800 rounded-md cursor-pointer">
                    {#if files === undefined}
                        Choose File
                    {:else}
                        {files[0].name}
                    {/if}
                </label>
                <input class="hidden" bind:files id="file" name="file" type="file"/>
            </div>
            <div class="flex justify-between items-center">
                <p class="h-fit text-xl">
                    Template
                </p>
                <select class="p-2 w-fit border border-sky-800 rounded-md" bind:value={template}>
                    {#await loadDatasetTemplates() then response}
                        {#each response.data as template}
                            <option value={template}>{template}</option>
                        {/each}
                    {/await}
                </select>
            </div>
            <div class="mt-3 w-full flex justify-center items-center">
                <button class="p-2 w-36 border border-sky-200 bg-sky-800 rounded-md text-white disabled:bg-sky-800/70"
                        {disabled} on:click={upload}>
                    Upload
                </button>
            </div>
        </div>
    </div>
{/if}