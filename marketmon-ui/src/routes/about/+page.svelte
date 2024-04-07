<script lang="ts">
import type { PageServerData } from "./$types";
import Card from "../Card.svelte";
  import Navbar from "../Navbar.svelte";

export let data: PageServerData;

</script>
    
<div
    class="min-h-screen bg-gradient-to-b from-blue-900 to-blue-500 text-white font-poppins"
  >
    <Navbar/>
<div>Story here</div>
    
</div>
