<template>
  <footer class="footer">
    <div class="container">
      <nav>
        <ul>
          <li>
            <a href="#/">Home</a>
          </li>
          <li>
            <router-link to="/about">
              About Us
            </router-link>
          </li>
        </ul>
      </nav>
      <div class="copyright text-center">
        &copy; {{ new Date().getFullYear() }}
        <a href="https://www.uprm.edu/cse/" target="_blank">
          University of Puerto Rico at Mayaguez </a
        >, made with <i class="fa fa-heart heart"></i>
      </div>
    </div>
  </footer>
</template>
<script>
export default {};
</script>
<style></style>
