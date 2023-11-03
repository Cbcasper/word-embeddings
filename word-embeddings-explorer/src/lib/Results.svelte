<script>
    import axios from "axios";
    import { get, writable } from "svelte/store";
    import Ranking from "./Ranking.svelte";
    import ControlPanel from "./ControlPanel.svelte";
    import MdAdd from "svelte-icons/md/MdAdd.svelte";

    export let article;
    export let parameters;

    let rankings = [];
    let selectedIndex;
    let internalUpdate = false;

    function select(index)
    {
        deselect();
        internalUpdate = true;
        article.set(rankings[index].article);
        parameters.set(rankings[index].parameters);
        internalUpdate = false;
        rankings[index] = {...rankings[index], selected: true};
        selectedIndex = index;
    }

    function deselect()
    {
        for (let [index, ranking] of rankings.entries())
            rankings[index] = {...ranking, selected: false};
    }

    function makeRanking()
    {
        return {
            loadStatus: "loading",
            article: get(article),
            parameters: get(parameters),
            selected: true,
        };
    }

    function add()
    {
        let newIndex = rankings.length;
        rankings = [...rankings, makeRanking()];
        select(newIndex);
        update();
    }

    function loadRanking()
    {
        let url = "http://127.0.0.1:5000/ranking";
        let data = { article: get(article).content };
        let config = {
            params: {
                ...get(parameters),
                fields: "v2"
            }
        };
        return axios.post(url, data, config);
    }

    function update()
    {
        if (internalUpdate)                                                 return;
        if (rankings.length === 0)                                          return;
        if (get(article) === undefined || get(parameters) === undefined)    return;

        rankings[selectedIndex] = {
            ...rankings[selectedIndex],
            article: get(article),
            parameters: get(parameters),
            loadStatus: "loading"
        };
        loadRanking().then(response => {
                        rankings[selectedIndex] = {
                            ...rankings[selectedIndex],
                            loadStatus: "ranking",
                            ranking: response.data.ranking.reverse(),
                            reverse: response.data.similarity_parameters.reverse
                        };
                    });
    }
    article.subscribe(update);
    parameters.subscribe(update);
</script>

<div class="h-full w-full flex p-2 gap-2 overflow-scroll relative">
    {#each rankings as ranking, index}
        <Ranking {...ranking} on:select={() => { select(index); }}></Ranking>
    {/each}
    <button class="w-10 h-10 absolute top-0 right-0 bg-white border-b-2 border-l-2 rounded-bl-md border-sky-800 text-sky-800"
            on:click={add}>
        <MdAdd/>
    </button>
</div>