<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Favicon -->
  <link rel="shortcut icon" href="{% static 'images/favicon.png' %}" type="image/x-icon" />
  <!-- Icon - IconMonster >
  <link rel="stylesheet" href="https://cdn.iconmonstr.com/1.3.0/css/iconmonstr-iconic-font.min.css" /-->
  <!-- Mumble UI -->
  <link rel="stylesheet" href="{% static 'uikit/styles/uikit.css' %}" />
  <!-- Dev Search UI -->
  <link rel="stylesheet" href="{% static 'css/app.css' %}" />

  <title>sst playground</title>
</head>


<body>

 <header class="header">
    <div class="container container--narrow">
      <a href="{% url 'profiles' %}" class="header__logo">
        <img src="{% static '/images/favicon.png' %}" alt="DevSearch Logo" />
      </a>
      <nav class="header__nav">
        <input type="checkbox" id="responsive-menu" />
        <label for="responsive-menu" class="toggle-menu">
          <span>Menu</span>
          <div class="toggle-menu__lines"></div>
        </label>
        <ul class="header__menu">
          <li class="header__menuItem"><a href="{% url 'profiles' %}">Profiles</a></li>
          <li class="header__menuItem"><a href="{% url 'home' %}">Projects</a></li>
          {% if request.user.is_authenticated %}
          <li class="header__menuItem"><a href="{% url 'inbox' %}">Inbox</a></li>
          <li class="header__menuItem"><a href="{% url 'account' %}">Account</a></li>
          <li class="header__menuItem"><a href="{% url 'logout' %}" class="btn btn--sub">Logout</a></li>
          {% else %}
          <li class="header__menuItem"><a href="{% url 'login' %}" class="btn btn--sub">Login/Sign Up</a></li>
          {% endif %}
        </ul>
      </nav>
    </div>
  </header>



{% if messages %}


{% for message in messages %}
    <div class="alert alert--{{message.tags}}">
    <!-- აი ამ ზედა ხაზის კალსის მეორე ჩანაწერი განასხვავებს ალერტ მესიჯის ტიპს და მერე
     ალერტის შესაბამისი ფერით გამოიტანს ალერტის ტექსტს. ფერებმა რომ იმუშაოს views.py-ში უნდა დავწეროთ მესიჯის
     სხვავდასხვა ტიპები. ანუ მარტო messages.error არა, ან მარტო messages.info-იც არა, არამედ მესიჯის ტიპის შესაბამისი-->
        <p class="alert__message">{{ message }}</p>
        <button class="alert__close">X</button>
    </div>
{% endfor %}
{% endif %}

<!--  ეს ზედა რამდენიმე ხაზი აკეთებს views-სთან ერთდად ასეთ რამმეს:
            თუ იუზერი შეცდომით ჩაწერს სახელს ან პაროლს ეს გამოუტანს ტექტს რომ
            მომხმარებლის სახელი ან პაროლი შეცდომითაა ჩაწერილი /-->


{% block tani  %}


{% endblock %}


</body>
<script src="{% static 'uikit/app.js' %}"></script>
<script src="{% static 'js/main.js' %}"></script>
</html>
