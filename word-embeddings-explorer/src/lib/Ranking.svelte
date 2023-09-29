<script>
    import { tick } from "svelte";

    export let fields;

    $: maxScore = fields === undefined ? 0 : Math.max(...fields.map(field => field.score)) + .15;

    // License: MIT - https://opensource.org/licenses/MIT
    // Author: Michele Locati <michele@locati.it>
    // Source: https://gist.github.com/mlocati/7210513
    function percentToColor(score)
    {
        let percent = score * 100 / maxScore;
        let red, green, blue = 0;
        if (percent < 50)
        {
            red = 255;
            green = Math.round(5.1 * percent);
        }
        else
        {
            green = 255;
            red = Math.round(510 - 5.10 * percent);
        }
        return [red, green, blue].join(", ");
    }

    let round = (number, digits) => Math.round(number * Math.pow(10, digits)) / Math.pow(10, digits);
</script>

<div class="h-full p-1 grid grid-cols-4">
    {#if fields !== undefined}
        {#each fields as field}
            <div class="p-2 flex justify-between border border-sky-100">
                <div class="p-1 h-fit my-auto">
                    {field.field}
                </div>
                <div class="py-1 px-2 rounded-md" style="background-color: rgb({percentToColor(field.score)}, .85)">
                    {round(field.score, 4)}
                </div>
            </div>
        {/each}
    {/if}
</div>