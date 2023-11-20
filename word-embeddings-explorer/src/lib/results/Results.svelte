<script>
    import { tick } from "svelte";
    import { get, writable } from "svelte/store";
    import FaCheck from "svelte-icons/fa/FaCheck.svelte";
    import FaFileAlt from "svelte-icons/fa/FaFileAlt.svelte";
    import FaAlignLeft from "svelte-icons/fa/FaAlignLeft.svelte";
    import FaChartLine from "svelte-icons/fa/FaChartLine.svelte";

    import Field from "./Field.svelte";
    import Ranking from "./Ranking.svelte";
    import Document from "./Document.svelte";
    import AddButton from "./AddButton.svelte";
    import Accuracies from "./Accuracies.svelte";

    import { article } from "../stores.js";

    let articleSelected;
    article.subscribe(value => articleSelected = value !== undefined);

    let results = [];

    function select(result)
    {
        deselect();
        result.selected = true;
    }

    function deselect()
    {
        for (let [index, result] of results.entries())
            results[index].selected = false;
    }

    function addRanking(rankingID)
    {
        let newRanking = { status: "loading", type: `${rankingID}-ranking`, rankingID };
        results = [...results, newRanking];
        select(newRanking);
    }

    function addAccuracies()
    {
        let newAccuracies = { status: "loading", type: "accuracies" };
        results = [...results, newAccuracies];
        select(newAccuracies);
    }
</script>

<div class="h-full w-full flex">
    <div class="h-full w-full p-2 gap-2 flex overflow-scroll">
        {#each results as result}
            {#if result.type === "field-ranking"}
                <Field bind:ranking={result} on:select={() => { select(result); }}/>
            {:else if result.type === "document-ranking"}
                <Document bind:ranking={result} on:select={() => { select(result); }}/>
            {:else if result.type === "accuracies"}
                <Accuracies bind:accuracies={result} on:select={() => { select(result); }}/>
            {/if}
        {/each}
    </div>
    <div class="h-full w-48 border-l-2 border-sky-800 divide-y-2 divide-sky-800 flex flex-col text-lg">
        <AddButton on:click={() => { addRanking("field"); }} disabled={!articleSelected}>
            <FaAlignLeft slot="button"/>
            <svelte:fragment slot="title">
                Field Ranking
            </svelte:fragment>
        </AddButton>
        <AddButton on:click={() => { addRanking("document"); }} disabled={!articleSelected}>
            <FaFileAlt slot="button"/>
            <svelte:fragment slot="title">
                Article Ranking
            </svelte:fragment>
        </AddButton>
        <AddButton on:click={() => { addAccuracies(); }} disabled={true}>
            <FaCheck slot="button"/>
            <svelte:fragment slot="title">
                Evaluate Ranking
            </svelte:fragment>
        </AddButton>
        <AddButton on:click={() => {}} disabled={true}>
            <FaChartLine slot="button"/>
            <svelte:fragment slot="title">
                Train Baseline
            </svelte:fragment>
        </AddButton>
    </div>
</div>