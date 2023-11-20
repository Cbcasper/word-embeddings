<script>
    import { Modals, closeModal } from "svelte-modals";
    import Workflow from "./lib/Workflow.svelte";
    import Results from "./lib/results/Results.svelte";
    import ControlPanel from "./lib/controlPanel/ControlPanel.svelte";

    let addEvaluation;
</script>

<main class="w-screen h-screen divide-y-2 divide-sky-800">
    <div class="w-full h-3/5 flex divide-x-2 divide-sky-800">
        <Workflow/>
        <div class="flex-none w-48">
            <ControlPanel></ControlPanel>
        </div>
    </div>
    <div class="h-2/5 w-full">
        <Results></Results>
    </div>
</main>

<Modals>
    <button slot="backdrop" class="fixed inset-0 bg-black opacity-50" on:click={closeModal}/>
</Modals>
