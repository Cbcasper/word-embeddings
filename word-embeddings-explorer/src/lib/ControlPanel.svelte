<script>
    import axios from "axios";
    import { tick, createEventDispatcher, onMount } from "svelte";

    import Ranking from "./Ranking.svelte";
    import ButtonPanel from "./ButtonPanel.svelte";

    export let parameters;

    let fields;
    let tab = "embeddings";
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

<div class="flex-none w-96 flex flex-col">
    <div class="flex divide-x-2 divide-sky-800 border-b-2 border-sky-800">
        <button class="flex-auto p-2 hover:bg-slate-200" on:click={() => tab = "embeddings"}
                class:bg-slate-300={tab === "embeddings"}>
            Embedding - <span class="font-semibold">{selectedEmbedding}</span>
        </button>
        <button class="flex-auto p-2 hover:bg-slate-200" on:click={() => tab = "similarities"}
                class:bg-slate-300={tab === "similarities"}>
            Similarity - <span class="font-semibold">{selectedSimilarity}</span>
        </button>
    </div>
    {#await loadEmbeddings() then embeddings}
        <div class="m-3" class:hidden={tab !== "embeddings"}>
            <ButtonPanel options={embeddings.data} on:select={select} bind:selectedOption={selectedEmbedding}></ButtonPanel>
        </div>
    {/await}
    {#await loadSimilarities() then similarities}
        <div class="m-3" class:hidden={tab !== "similarities"}>
            <ButtonPanel options={similarities.data} on:select={select} bind:selectedOption={selectedSimilarity}></ButtonPanel>
        </div>
    {/await}
</div>