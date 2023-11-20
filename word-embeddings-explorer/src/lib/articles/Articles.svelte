<script>
    import axios from "axios";
    import { tick } from "svelte";

    import { openModal } from "svelte-modals";
    import FaFileUpload from "svelte-icons/fa/FaFileUpload.svelte";

    import DatasetUpload from "./DatasetUpload.svelte";
    import { article, dataset } from "../stores.js";

    let articles = [];
    let datasets = [];
    let datasetSelect;

    function selectArticle(selectedArticle)
    {
        article.set(selectedArticle);
    }

    function updateDataset(data)
    {
        let newDataset = data.data;
        dataset.set({
            id: newDataset.id,
            title: newDataset.title,
            filename: newDataset.filename,
        });
        articles = newDataset.articles;
    }

    function selectDataset(selectedDataset)
    {
        datasetSelect.value = selectedDataset;
        let url = "http://127.0.0.1:5000/dataset";
        let config = { params: { dataset: selectedDataset } };
        axios.get(url, config).then(updateDataset);
    }

    function loadDatasets()
    {
        let url = "http://127.0.0.1:5000/datasets";
        return axios.get(url).then(response => { datasets = response.data; })
    }
    loadDatasets().then(() => { selectDataset(datasets[0]); });

    function openUpload()
    {
        openModal(DatasetUpload, { loadDatasets, selectDataset });
    }
</script>

<div class="h-full w-full flex flex-col border-l-8 border-sky-800">
    <div class="w-full p-3 border-b-2 border-sky-800 flex justify-between">
        <samp>
            <select on:change={event => { selectDataset(event.target.value); }}
                    bind:this={datasetSelect}>
                {#each datasets as dataset}
                    <option value={dataset}>{dataset}</option>
                {/each}
            </select>
        </samp>
        <button class="mx-2 h-6 text-sky-800" on:click={openUpload}>
            <FaFileUpload/>
        </button>
    </div>
    <div class="grow w-full divide-y divide-sky-100 overflow-scroll">
        {#each articles as listedArticle}
            <button class:bg-slate-300={$article === listedArticle}
                    class="w-full px-2 py-0.5 text-ellipsis text-left whitespace-nowrap overflow-hidden
                        hover:bg-slate-200"
                    on:click={() => selectArticle(listedArticle)}>
                {listedArticle.title}
            </button>
        {/each}
    </div>
</div>