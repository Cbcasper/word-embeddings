<script>
    import axios from "axios";
    import { tick, createEventDispatcher, onMount } from "svelte";

    import Ranking from "./Ranking.svelte";
    import ButtonPanel from "./ButtonPanel.svelte";

    export let parameters;

    let fields;
    let selectedEmbedding;
    let selectedSimilarity;
    const dispatch = createEventDispatcher();

    let loadEmbeddings = () => axios.get("http://127.0.0.1:5000/embeddings");
    let loadSimilarities = () => axios.get("http://127.0.0.1:5000/similarities");

    function setParameters()
    {
        parameters = {
            embedding: selectedEmbedding,
            similarity: selectedSimilarity,
        };
    }

    async function select()
    {
        await tick();
        setParameters();
        dispatch("select");
    }
</script>

<div class="flex-none w-48 flex flex-col divide-y-2 divide-sky-800">
    {#await loadEmbeddings() then embeddings}
        <div class="h-1/2 divide-y-2 divide-sky-800">
            <div class="p-3 text-xl">Embedding</div>
            <ButtonPanel options={embeddings.data} on:select={select} bind:selectedOption={selectedEmbedding}></ButtonPanel>
        </div>
    {/await}
    {#await loadSimilarities() then similarities}
        <div class="h-1/2 divide-y-2 divide-sky-800">
            <div class="p-3 text-xl">Similarity</div>
            <ButtonPanel options={similarities.data} on:select={select} bind:selectedOption={selectedSimilarity}></ButtonPanel>
        </div>
    {/await}
</div>