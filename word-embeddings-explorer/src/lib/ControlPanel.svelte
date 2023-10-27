<script>
    import axios from "axios";
    import { get, writable } from "svelte/store";
    import { tick, createEventDispatcher, onMount } from "svelte";
    import ButtonPanel from "./ButtonPanel.svelte";

    export let parameters;

    let fields;
    let selectedEmbedding;
    let selectedSimilarity;

    let parameterConfig = [
        {
            url: "embeddings",
            id: "embedding",
            title: "Embedding",
            value: writable()
        },
        {
            url: "similarities",
            id: "similarity",
            title: "Similarity",
            value: writable()
        }
    ];
    let load = parameterType => axios.get(`http://127.0.0.1:5000/${parameterType}`);
    let getParameters = (result, parameter) => ({...result, [parameter.id]: get(parameter.value)});
    
    function setParameters()
    {
        if (parameterConfig.every(parameter => get(parameter.value) !== undefined))
            parameters.set(parameterConfig.reduce(getParameters, {}));
    }
    for (let parameter of parameterConfig)
        parameter.value.subscribe(setParameters);
</script>

<div class="flex-none w-48 flex flex-col divide-y-2 divide-sky-800">
    {#each parameterConfig as parameter}
        {#await load(parameter.url) then options}
            <div class="h-1/2 divide-y-2 divide-sky-800">
                <div class="p-3 text-xl">{parameter.title}</div>
                <ButtonPanel options={options.data} parameter={parameter.value}></ButtonPanel>
            </div>
        {/await}
    {/each}
</div>