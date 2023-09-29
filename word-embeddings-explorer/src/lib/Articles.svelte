<script>
    import { createEventDispatcher } from "svelte";

    export let articles;

    let selectedArticle;
    const dispatch = createEventDispatcher();

    function select(article)
    {
        dispatch('select', article);
        selectedArticle = article;
    }
</script>

<div class="divide-y divide-sky-100 border-r-2 border-l-8 border-sky-800">
    {#each articles as article}
        <button class:bg-slate-300={selectedArticle === article.article}
                class="w-full px-1 py-0.5 text-ellipsis text-left whitespace-nowrap overflow-hidden
                       hover:bg-slate-200"
                on:click={() => select(article.article)}>
            {article.article.title}
        </button>
    {/each}
</div>