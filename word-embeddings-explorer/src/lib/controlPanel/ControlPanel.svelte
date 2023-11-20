<script>
    import axios from "axios";
    import { get, writable } from "svelte/store";
    import { tick, createEventDispatcher, onMount } from "svelte";

    import { parameters } from "../stores.js";
    import ButtonPanel from "./ButtonPanel.svelte";

    let embedding;
    let similarity;
    let loadEmbeddings = () => axios.get("http://127.0.0.1:5000/embeddings");
    let loadSimilarities = () => axios.get("http://127.0.0.1:5000/similarities");

    function update(updateValue)
    {
        if (updateValue !== undefined)
        {
            embedding = updateValue.embedding;
            similarity = updateValue.similarity;
        }
    }
    parameters.subscribe(update);
    
    function select()
    {
        if (embedding !== undefined && similarity != undefined)
            parameters.set({ embedding, similarity });
    }
</script>

<div class="w-full h-full flex flex-col divide-y-2 divide-sky-800">
    {#await loadEmbeddings() then options}
        <div class="h-1/2 divide-y-2 divide-sky-800">
            <div class="p-3 text-xl">Embeddings</div>
            <ButtonPanel options={options.data} bind:selected={embedding} on:select={select}></ButtonPanel>
        </div>
    {/await}
    {#await loadSimilarities() then options}
        <div class="h-1/2 divide-y-2 divide-sky-800">
            <div class="p-3 text-xl">Similarities</div>
            <ButtonPanel options={options.data} bind:selected={similarity} on:select={select}></ButtonPanel>
        </div>
    {/await}
</div>