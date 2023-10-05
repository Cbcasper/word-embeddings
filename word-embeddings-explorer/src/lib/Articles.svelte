<script>
    import axios from "axios";
    import { createEventDispatcher } from "svelte";

    export let selectedArticle;

    const dispatch = createEventDispatcher();

    let loadArticles = () => axios.get("http://127.0.0.1:5000/articles");
    function select(article)
    {
        selectedArticle = article;
        dispatch('select');
    }
</script>

<div class="divide-y divide-sky-100 border-r-2 border-l-8 border-sky-800">
    {#await loadArticles() then data}
        {#each data.data as article}
            <button class:bg-slate-300={selectedArticle === article.article}
                    class="w-full px-2 py-0.5 text-ellipsis text-left whitespace-nowrap overflow-hidden
                        hover:bg-slate-200"
                    on:click={() => select(article.article)}>
                {article.article.title}
            </button>
        {/each}
    {/await}
</div>