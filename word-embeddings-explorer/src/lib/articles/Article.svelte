<script>
    import axios from "axios";
    import MdEdit from "svelte-icons/md/MdEdit.svelte";
    import MdCheck from "svelte-icons/md/MdCheck.svelte";

    import { article } from "../stores.js";
    import Classification from "./Classification.svelte";

    let displayArticle;
    let classification;

    let editing = false;
    let hovering = false;

    function update(updateValue)
    {
        let previousArticle = displayArticle;
        displayArticle = updateValue;
        editing = false;
        
        if (displayArticle !== undefined && displayArticle !== previousArticle)
            classification = classifyArticle();
    }
    article.subscribe(update);

    function classifyArticle()
    {
        let url = "http://127.0.0.1:5000/classification";
        let data = { article: displayArticle.content };
        let config = {
            params: {}
        };
        return axios.post(url, data, config);
    }

    let updateContent = event => { displayArticle.content = event.target.value; };
    function edit()
    {
        editing = true;
        displayArticle = { content: "", title: "Write your own article!" };
    }

    function submit()
    {
        article.set(displayArticle);
        editing = true;
    }
</script>

<article class="h-full w-full flex flex-col relative"
        on:mouseenter={() => hovering = true} on:mouseleave={() => hovering = false}>
    {#if displayArticle !== undefined}
        <div class="mt-4 mx-4 pb-2 text-2xl border-b-2 border-sky-600">
            {displayArticle.title}
        </div>
        {#if !editing}
            {#if displayArticle.subTitle !== null}
                <div class="mx-4 text-xl">
                    {displayArticle.subTitle}
                </div>
            {/if}
            <div class="grow mx-4 py-2 overflow-scroll text-ellipsis">
                {displayArticle.content}
            </div>
        {:else}
            <textarea class="grow mx-4 my-2 p-2 focus:outline-dashed focus:outline-2 focus:outline-sky-600 rounded-md"
                    placeholder="Start writing!" on:input={updateContent}></textarea>
        {/if}
        <div class="border-t-2 border-sky-800 divide-x-2 divide-sky-800 flex">
            <Classification styling="p-4 w-1/3 flex-none" title="Fields Of Interest" field={displayArticle.fieldsOfInterest}/>
            <Classification styling="p-4 w-1/3 flex-none" title="Keywords" field={displayArticle.keywords}/>
            {#await classification then response}
                <Classification styling="p-4 w-1/3 grow" title="Classification" field={response.data.classification}/>
            {/await}
        </div>
    {:else}
        <div class="mt-4 mx-4 font-bold">
            Select an article to begin
        </div>
    {/if}
    <button class="pt-1 pr-1 pb-2 pl-2 w-10 h-10 absolute top-0 right-0 bg-white
                border-b-2 border-l-2 rounded-bl-md border-sky-800 text-sky-800"
            class:hidden={!(hovering && !editing)} on:click={edit}>
        <MdEdit/>
    </button>
    <button class="pt-1 pr-1 pb-2 pl-2 w-10 h-10 absolute top-0 right-0 bg-white
                border-b-2 border-l-2 rounded-bl-md border-sky-800 text-sky-800"
            class:hidden={!(hovering && editing)} on:click={submit}>
        <MdCheck/>
    </button>
</article>