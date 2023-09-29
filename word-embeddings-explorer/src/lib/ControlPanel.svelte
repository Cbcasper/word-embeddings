<script>
    import axios from "axios";
    import { tick } from "svelte";

    import Ranking from "./Ranking.svelte";
    import ButtonPanel from "./ButtonPanel.svelte";

    export let article;

    let fields;
    let selectedEmbedding;
    let selectedSimilarity;

    let loadEmbeddings = () => axios.get("http://127.0.0.1:5000/embeddings");
    let loadSimilarities = () => axios.get("http://127.0.0.1:5000/similarities");

    async function update()
    {
        await tick()
        let config = {
            params: {
                id: article.id,
                embedding: selectedEmbedding,
                similarity: selectedSimilarity
            }
        };
        axios.get("http://127.0.0.1:5000/ranking", config)
             .then(response => fields = response.data);
    }
</script>

<div class="h-1/2 space-y-1 flex flex-col">
    {#await loadEmbeddings() then embeddings}
        <div class="mx-2">
            <ButtonPanel title="Choose an embedding:" options={embeddings.data}
                        on:select={update} bind:selectedOption={selectedEmbedding}></ButtonPanel>
        </div>
    {/await}
    {#await loadSimilarities() then similarities}
        <div class="mx-2">
            <ButtonPanel title="Choose a similarity:" options={similarities.data}
                        on:select={update} bind:selectedOption={selectedSimilarity}></ButtonPanel>
        </div>
    {/await}
    <div class="grow overflow-scroll">
        <Ranking {fields}></Ranking>
    </div>
</div>