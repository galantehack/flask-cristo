from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import datetime
import requests


app = Flask(__name__)





# Diccionario de versículos para cada sentimiento
verses = {
    "feliz": [
    "Salmos 118:24 - Este es el día que hizo el Señor; nos gozaremos y alegraremos en él.",
    "Nehemías 8:10 - No os entristezcáis, porque el gozo del Señor es nuestra fortaleza.",
    "Filipenses 4:4 - Alegraos en el Señor siempre. Otra vez digo: Alegraos.",
    "Proverbios 17:22 - El corazón alegre es buena medicina, pero el espíritu quebrantado seca los huesos.",
    "Salmos 16:11 - Me mostrarás la senda de la vida; en tu presencia hay plenitud de gozo; delicias a tu diestra para siempre.",
    "Romanos 15:13 - Y el Dios de esperanza os llene de todo gozo y paz en el creer, para que abundéis en esperanza por el poder del Espíritu Santo.",
    "Juan 15:11 - Estas cosas os he hablado, para que mi gozo esté en vosotros, y vuestro gozo sea completo.",
    "Salmos 37:4 - Deléitate asimismo en el Señor, y él te concederá las peticiones de tu corazón.",
    "1 Tesalonicenses 5:16-18 - Estad siempre gozosos. Orad sin cesar. Dad gracias en todo, porque esta es la voluntad de Dios para con vosotros en Cristo Jesús.",
    "Salmos 126:3 - Grandes cosas ha hecho el Señor con nosotros; estaremos alegres.",
    "Salmos 30:11 - Has cambiado mi lamento en baile; desataste mi cilicio y me ceñiste de alegría.",
    "Isaías 61:10 - En gran manera me gozaré en el Señor, mi alma se alegrará en mi Dios; porque me vistió con vestiduras de salvación, me rodeó de manto de justicia.",
    "Salmos 32:11 - Alegraos en el Señor y gozaos, justos; cantad con júbilo todos vosotros los rectos de corazón.",
    "Salmos 144:15 - Bienaventurado el pueblo que tiene esto; bienaventurado el pueblo cuyo Dios es el Señor.",
    "Efesios 5:19-20 - Hablando entre vosotros con salmos, con himnos y cánticos espirituales, cantando y alabando al Señor en vuestros corazones; dando siempre gracias por todo al Dios y Padre, en el nombre de nuestro Señor Jesucristo.",
    "Salmos 100:2 - Servid al Señor con alegría; venid ante su presencia con regocijo.",
    "1 Pedro 1:8 - A quien amáis sin haberle visto, en quien creyendo, aunque ahora no lo veáis, os alegráis con gozo inefable y glorioso.",
    "Salmos 92:4 - Porque tú, Señor, me has alegrado con tus obras; en las obras de tus manos me gozo.",
    "Isaías 12:3 - Sacaréis con gozo aguas de las fuentes de la salvación.",
    "Filipenses 2:17-18 - Y aunque sea derramado en libación sobre el sacrificio y servicio de vuestra fe, me gozo y regocijo con todos vosotros. Y asimismo gozaos y regocijaos también vosotros conmigo."
    ],
    "triste": [
    "Mateo 5:4 - Bienaventurados los que lloran, porque ellos recibirán consolación.",
    "2 Corintios 1:3-4 - Bendito sea el Dios y Padre de nuestro Señor Jesucristo, Padre de misericordias y Dios de toda consolación, quien nos consuela en todas nuestras tribulaciones.",
    "Salmos 34:18 - Cercano está el Señor a los quebrantados de corazón; y salva a los contritos de espíritu.",
    "Salmos 147:3 - Él sana a los quebrantados de corazón y venda sus heridas.",
    "Juan 16:20 - De cierto, de cierto os digo, que lloraréis y lamentaréis, y el mundo se alegrará; pero aunque vosotros estéis tristes, vuestra tristeza se convertirá en gozo.",
    "Apocalipsis 21:4 - Enjugará Dios toda lágrima de los ojos de ellos; y no habrá más muerte, ni habrá más llanto, ni clamor, ni dolor; porque las primeras cosas pasaron.",
    "Salmos 42:11 - ¿Por qué te abates, oh alma mía, y por qué te turbas dentro de mí? Espera en Dios; porque aún he de alabarle, salvación mía y Dios mío.",
    "Isaías 41:10 - No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te esfuerzo; siempre te ayudaré, siempre te sustentaré con la diestra de mi justicia.",
    "Lamentaciones 3:22-23 - Por la misericordia del Señor no hemos sido consumidos, porque nunca decayeron sus misericordias. Nuevas son cada mañana; grande es tu fidelidad.",
    "Salmos 30:5 - Porque un momento será su ira, pero su favor dura toda la vida. Por la noche durará el lloro, y a la mañana vendrá la alegría.",
    "Isaías 40:31 - Pero los que esperan a Jehová tendrán nuevas fuerzas; levantarán alas como las águilas; correrán, y no se cansarán; caminarán, y no se fatigarán.",
    "Romanos 8:18 - Pues tengo por cierto que las aflicciones del tiempo presente no son comparables con la gloria venidera que en nosotros ha de manifestarse.",
    "Salmos 55:22 - Echa sobre el Señor tu carga, y él te sustentará; no dejará para siempre caído al justo.",
    "Isaías 43:2 - Cuando pases por las aguas, yo estaré contigo; y si por los ríos, no te anegarán; cuando pases por el fuego, no te quemarás, ni la llama arderá en ti.",
    "Filipenses 4:6-7 - Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias. Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.",
    "Salmos 23:4 - Aunque ande en valle de sombra de muerte, no temeré mal alguno, porque tú estarás conmigo; tu vara y tu cayado me infundirán aliento.",
    "Jeremías 29:11 - Porque yo sé los pensamientos que tengo acerca de vosotros, dice el Señor, pensamientos de paz, y no de mal, para daros el fin que esperáis.",
    "1 Pedro 5:7 - Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.",
    "Salmos 56:8 - Mis huidas tú has contado; pon mis lágrimas en tu redoma; ¿no están ellas en tu libro?"
    ],
    "enojo": [
    "Efesios 4:26 - Airaos, pero no pequéis; no se ponga el sol sobre vuestro enojo.",
    "Proverbios 15:1 - La blanda respuesta quita la ira, mas la palabra áspera hace subir el furor.",
    "Santiago 1:19-20 - Por esto, mis amados hermanos, todo hombre sea pronto para oír, tardo para hablar, tardo para airarse; porque la ira del hombre no obra la justicia de Dios.",
    "Proverbios 29:11 - El necio da rienda suelta a toda su ira, mas el sabio al fin la sosiega.",
    "Colosenses 3:8 - Pero ahora dejad también vosotros todas estas cosas: ira, enojo, malicia, blasfemia, palabras deshonestas de vuestra boca.",
    "Proverbios 19:11 - La cordura del hombre detiene su furor, y su honra es pasar por alto la ofensa.",
    "Salmos 37:8 - Deja la ira y desecha el enojo; no te excites en manera alguna a hacer lo malo.",
    "Eclesiastés 7:9 - No te apresures en tu espíritu a enojarte, porque el enojo reposa en el seno de los necios.",
    "Proverbios 16:32 - Mejor es el que tarda en airarse que el fuerte, y el que se enseñorea de su espíritu, que el que toma una ciudad.",
    "Mateo 5:22 - Pero yo os digo que cualquiera que se enoje contra su hermano, será culpable de juicio; y cualquiera que diga: Necio, a su hermano, será culpable ante el concilio; y cualquiera que le diga: Fatuo, quedará expuesto al infierno de fuego.",
    "Romanos 12:19 - No os venguéis vosotros mismos, amados míos, sino dejad lugar a la ira de Dios; porque escrito está: Mía es la venganza, yo pagaré, dice el Señor.",
    "Efesios 4:31 - Quítense de vosotros toda amargura, enojo, ira, gritería y maledicencia, y toda malicia.",
    "Proverbios 14:29 - El que tarda en airarse es grande de entendimiento; mas el que es impaciente de espíritu enaltece la necedad.",
    "Salmos 86:15 - Mas tú, Señor, Dios misericordioso y clemente, lento para la ira y grande en misericordia y verdad.",
    "Proverbios 22:24-25 - No te entremetas con el iracundo, ni te acompañes con el hombre de enojos, no sea que aprendas sus maneras, y tomes lazo para tu alma.",
    "Romanos 12:21 - No seas vencido de lo malo, sino vence con el bien el mal.",
    "Proverbios 15:18 - El hombre iracundo promueve contiendas, pero el que tarda en airarse apacigua la rencilla.",
    "Gálatas 5:22-23 - Mas el fruto del Espíritu es amor, gozo, paz, paciencia, benignidad, bondad, fe, mansedumbre, templanza; contra tales cosas no hay ley.",
    "Salmos 4:4 - Temblad, y no pequéis; meditad en vuestro corazón estando en vuestra cama, y callad."
],
    "miedo": [
    "Isaías 41:10 - No temas, porque yo estoy contigo; no desmayes, porque yo soy tu Dios que te esfuerzo; siempre te ayudaré, siempre te sustentaré con la diestra de mi justicia.",
    "Salmos 56:3 - En el día que temo, yo en ti confío.",
    "2 Timoteo 1:7 - Porque no nos ha dado Dios espíritu de cobardía, sino de poder, de amor y de dominio propio.",
    "Salmos 23:4 - Aunque ande en valle de sombra de muerte, no temeré mal alguno, porque tú estarás conmigo; tu vara y tu cayado me infundirán aliento.",
    "Deuteronomio 31:6 - Esforzaos y cobrad ánimo; no temáis, ni tengáis miedo de ellos, porque el Señor tu Dios es el que va contigo; no te dejará, ni te desamparará.",
    "Salmos 27:1 - El Señor es mi luz y mi salvación; ¿de quién temeré? El Señor es la fortaleza de mi vida; ¿de quién he de atemorizarme?",
    "Juan 14:27 - La paz os dejo, mi paz os doy; yo no os la doy como el mundo la da. No se turbe vuestro corazón, ni tenga miedo.",
    "Josué 1:9 - Mira que te mando que te esfuerces y seas valiente; no temas ni desmayes, porque el Señor tu Dios estará contigo en dondequiera que vayas.",
    "Salmos 34:4 - Busqué al Señor, y él me oyó, y me libró de todos mis temores.",
    "Isaías 35:4 - Decid a los de corazón apocado: Esforzaos, no temáis; he aquí que vuestro Dios viene con retribución, con pago; Dios mismo vendrá y os salvará.",
    "1 Juan 4:18 - En el amor no hay temor, sino que el perfecto amor echa fuera el temor; porque el temor lleva en sí castigo. De donde el que teme, no ha sido perfeccionado en el amor.",
    "Salmos 91:5-6 - No temerás el terror nocturno, ni saeta que vuele de día, ni pestilencia que ande en oscuridad, ni mortandad que en medio del día destruya.",
    "Proverbios 3:24-26 - Cuando te acuestes, no tendrás temor, sino que te acostarás, y tu sueño será grato. No tendrás temor de pavor repentino, ni de la ruina de los impíos cuando viniere, porque el Señor será tu confianza, y él preservará tu pie de quedar preso.",
    "Romanos 8:15 - Pues no habéis recibido el espíritu de esclavitud para estar otra vez en temor, sino que habéis recibido el espíritu de adopción, por el cual clamamos: ¡Abba, Padre!",
    "Salmos 46:1-2 - Dios es nuestro amparo y fortaleza, nuestro pronto auxilio en las tribulaciones. Por tanto, no temeremos, aunque la tierra sea removida, y se traspasen los montes al corazón del mar.",
    "Isaías 43:1 - Ahora, así dice el Señor, creador tuyo, oh Jacob, y formador tuyo, oh Israel: No temas, porque yo te redimí; te puse nombre, mío eres tú.",
    "Mateo 10:29-31 - ¿No se venden dos pajarillos por un cuarto? Con todo, ni uno de ellos cae a tierra sin vuestro Padre. Pues aun vuestros cabellos están todos contados. Así que, no temáis; más valéis vosotros que muchos pajarillos.",
    "Filipenses 4:6-7 - Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias. Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.",
    "Salmos 112:7 - No tendrá temor de malas noticias; su corazón está firme, confiado en el Señor."
],
    "confianza": [
    "Proverbios 3:5-6 - Confía en el Señor con todo tu corazón, y no te apoyes en tu propia prudencia. Reconócelo en todos tus caminos, y él enderezará tus veredas.",
    "Salmos 37:5 - Encomienda al Señor tu camino, confía en él, y él hará.",
    "Jeremías 17:7-8 - Bendito el hombre que confía en el Señor, y cuya confianza es el Señor. Será como un árbol plantado junto a las aguas, que junto a la corriente echará sus raíces, y no verá cuando viene el calor, sino que su hoja estará verde; y en el año de sequía no se fatigará, ni dejará de dar fruto.",
    "Salmos 118:8-9 - Mejor es confiar en el Señor que confiar en el hombre. Mejor es confiar en el Señor que confiar en príncipes.",
    "Isaías 26:3-4 - Tú guardarás en completa paz a aquel cuyo pensamiento en ti persevera, porque en ti ha confiado. Confiad en el Señor perpetuamente, porque en el Señor Dios está la fortaleza eterna.",
    "Salmos 56:4 - En Dios alabaré su palabra, en Dios he confiado; no temeré. ¿Qué puede hacerme el hombre?",
    "Hebreos 10:35-36 - No perdáis, pues, vuestra confianza, que tiene grande galardón; porque os es necesaria la paciencia, para que habiendo hecho la voluntad de Dios, obtengáis la promesa.",
    "Salmos 91:2 - Diré yo al Señor: Esperanza mía, y castillo mío; mi Dios, en quien confiaré.",
    "Filipenses 1:6 - Estando persuadido de esto, que el que comenzó en vosotros la buena obra, la perfeccionará hasta el día de Jesucristo.",
    "2 Corintios 3:4-5 - Y tal confianza tenemos mediante Cristo para con Dios; no que seamos competentes por nosotros mismos para pensar algo como de nosotros mismos, sino que nuestra competencia proviene de Dios.",
    "Salmos 27:3 - Aunque un ejército acampe contra mí, no temerá mi corazón; aunque contra mí se levante guerra, yo estaré confiado.",
    "Romanos 8:28 - Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien, esto es, a los que conforme a su propósito son llamados.",
    "Isaías 12:2 - He aquí, Dios es mi salvación; confiaré, y no temeré; porque mi fortaleza y mi canción es el Señor, quien ha sido salvación para mí.",
    "2 Samuel 22:31 - En cuanto a Dios, perfecto es su camino, y acrisolada la palabra del Señor; escudo es a todos los que en él esperan.",
    "Salmos 46:10 - Estad quietos, y conoced que yo soy Dios; seré exaltado entre las naciones; enaltecido seré en la tierra.",
    "1 Pedro 5:7 - Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.",
    "Proverbios 16:3 - Encomienda al Señor tus obras, y tus pensamientos serán afirmados.",
    "Salmos 112:7 - No tendrá temor de malas noticias; su corazón está firme, confiado en el Señor.",
    "Isaías 30:15 - Porque así dijo el Señor Dios, el Santo de Israel: En descanso y en reposo seréis salvos; en quietud y en confianza será vuestra fortaleza."
],
    "verguenza": [
    "Salmos 25:2-3 - Dios mío, en ti confío; no sea yo avergonzado, no se alegren de mí mis enemigos. Ciertamente, ninguno de cuantos esperan en ti será confundido; serán avergonzados los que se rebelan sin causa.",
    "Isaías 54:4 - No temas, pues no serás confundida; y no te avergüences, porque no serás afrentada, sino que te olvidarás de la vergüenza de tu juventud, y de la afrenta de tu viudez no tendrás más memoria.",
    "Romanos 10:11 - Pues la Escritura dice: Todo aquel que en él creyere, no será avergonzado.",
    "Joel 2:26-27 - Comeréis hasta saciaros, y alabaréis el nombre del Señor vuestro Dios, que hizo maravillas con vosotros; y nunca jamás será mi pueblo avergonzado. Y conoceréis que en medio de Israel estoy yo, y que yo soy el Señor vuestro Dios, y no hay otro; y mi pueblo nunca jamás será avergonzado.",
    "Salmos 31:17 - No sea yo avergonzado, oh Señor, porque te he invocado; sean avergonzados los impíos, estén mudos en el Seol.",
    "Isaías 50:7 - Porque el Señor Dios me ayudará, por tanto no me avergoncé; por eso puse mi rostro como un pedernal, y sé que no seré avergonzado.",
    "1 Pedro 4:16 - Pero si alguno padece como cristiano, no se avergüence, sino glorifique a Dios por ello.",
    "Salmos 119:6 - Entonces no sería yo avergonzado, cuando atendiese a todos tus mandamientos.",
    "Romanos 1:16 - Porque no me avergüenzo del evangelio, porque es poder de Dios para salvación a todo aquel que cree; al judío primeramente, y también al griego.",
    "Salmos 69:6 - No sean avergonzados por causa de mí los que en ti confían, oh Señor Dios de los ejércitos; no sean confundidos por mí los que te buscan, oh Dios de Israel.",
    "Isaías 61:7 - En lugar de vuestra doble vergüenza, y de vuestra deshonra, os alabarán en sus heredades; por lo cual en sus tierras poseerán doble honra, y tendrán perpetuo gozo.",
    "Filipenses 1:20 - Conforme a mi anhelo y esperanza de que en nada seré avergonzado; antes bien, con toda confianza, como siempre, ahora también será magnificado Cristo en mi cuerpo, o por vida o por muerte.",
    "Salmos 44:15 - Todo el día mi vergüenza está delante de mí, y la confusión de mi rostro me cubre.",
    "Jeremías 17:13 - Oh Señor, esperanza de Israel, todos los que te dejan serán avergonzados; y los que se apartan de mí serán escritos en el polvo, porque dejaron al Señor, manantial de aguas vivas.",
    "2 Timoteo 1:12 - Por lo cual asimismo padezco esto, pero no me avergüenzo, porque yo sé a quién he creído, y estoy seguro que es poderoso para guardar mi depósito para aquel día.",
    "Proverbios 13:18 - Pobreza y vergüenza tendrá el que menosprecia el consejo; mas el que guarda la corrección recibirá honra.",
    "Salmos 34:5 - Los que miraron a él fueron alumbrados, y sus rostros no fueron avergonzados.",
    "Romanos 5:5 - Y la esperanza no avergüenza; porque el amor de Dios ha sido derramado en nuestros corazones por el Espíritu Santo que nos fue dado."
],
 "culpa": [
    "Salmos 32:5 - Mi pecado te declaré, y no encubrí mi iniquidad. Dije: Confesaré mis transgresiones al Señor; y tú perdonaste la maldad de mi pecado.",
    "1 Juan 1:9 - Si confesamos nuestros pecados, él es fiel y justo para perdonar nuestros pecados, y limpiarnos de toda maldad.",
    "Romanos 8:1 - Ahora, pues, ninguna condenación hay para los que están en Cristo Jesús, los que no andan conforme a la carne, sino conforme al Espíritu.",
    "Salmos 51:1-2 - Ten piedad de mí, oh Dios, conforme a tu misericordia; conforme a la multitud de tus piedades borra mis rebeliones. Lávame más y más de mi maldad, y límpiame de mi pecado.",
    "Isaías 1:18 - Venid luego, dice el Señor, y estemos a cuenta: si vuestros pecados fueren como la grana, como la nieve serán emblanquecidos; si fueren rojos como el carmesí, vendrán a ser como blanca lana.",
    "Salmos 103:12 - Cuanto está lejos el oriente del occidente, hizo alejar de nosotros nuestras rebeliones.",
    "Hebreos 8:12 - Porque seré propicio a sus injusticias, y nunca más me acordaré de sus pecados y de sus iniquidades.",
    "Miqueas 7:18-19 - ¿Qué Dios como tú, que perdona la maldad, y olvida el pecado del remanente de su heredad? No retuvo para siempre su enojo, porque se deleita en misericordia. Él volverá a tener misericordia de nosotros; sepultará nuestras iniquidades, y echará en lo profundo del mar todos nuestros pecados.",
    "2 Corintios 5:17 - De modo que si alguno está en Cristo, nueva criatura es; las cosas viejas pasaron; he aquí todas son hechas nuevas.",
    "Romanos 3:23-24 - Por cuanto todos pecaron, y están destituidos de la gloria de Dios, siendo justificados gratuitamente por su gracia, mediante la redención que es en Cristo Jesús.",
    "Hebreos 10:22 - Acerquémonos con corazón sincero, en plena certidumbre de fe, purificados los corazones de mala conciencia, y lavados los cuerpos con agua pura.",
    "Efesios 1:7 - En quien tenemos redención por su sangre, el perdón de pecados según las riquezas de su gracia.",
    "Salmos 130:3-4 - Señor, si miras los pecados, ¿quién, oh Señor, podrá mantenerse? Pero en ti hay perdón, para que seas reverenciado.",
    "1 Pedro 2:24 - Quien llevó él mismo nuestros pecados en su cuerpo sobre el madero, para que nosotros, estando muertos a los pecados, vivamos a la justicia; y por cuya herida fuisteis sanados.",
    "Isaías 53:5 - Mas él herido fue por nuestras rebeliones, molido por nuestros pecados; el castigo de nuestra paz fue sobre él, y por su llaga fuimos nosotros curados.",
    "Romanos 5:8 - Mas Dios muestra su amor para con nosotros, en que siendo aún pecadores, Cristo murió por nosotros.",
    "1 Corintios 15:3-4 - Porque primeramente os he enseñado lo que asimismo recibí: Que Cristo murió por nuestros pecados, conforme a las Escrituras; y que fue sepultado, y que resucitó al tercer día, conforme a las Escrituras.",
    "Colosenses 2:13-14 - Y a vosotros, estando muertos en pecados y en la incircuncisión de vuestra carne, os dio vida juntamente con él, perdonándoos todos los pecados, anulando el acta de los decretos que había contra nosotros, que nos era contraria, quitándola de en medio y clavándola en la cruz.",
    "Salmos 86:5 - Porque tú, Señor, eres bueno y perdonador, y grande en misericordia para con todos los que te invocan."
],
 "amor": [
    "1 Juan 4:8 - El que no ama, no conoce a Dios; porque Dios es amor.",
    "Juan 3:16 - Porque de tal manera amó Dios al mundo, que ha dado a su Hijo unigénito, para que todo aquel que en él cree, no se pierda, mas tenga vida eterna.",
    "1 Corintios 13:4-7 - El amor es sufrido, es benigno; el amor no tiene envidia, el amor no es jactancioso, no se envanece; no hace nada indebido, no busca lo suyo, no se irrita, no guarda rencor; no se goza de la injusticia, más se goza de la verdad; todo lo sufre, todo lo cree, todo lo espera, todo lo soporta.",
    "Romanos 5:8 - Mas Dios muestra su amor para con nosotros, en que siendo aún pecadores, Cristo murió por nosotros.",
    "1 Juan 4:9-10 - En esto se mostró el amor de Dios para con nosotros: en que Dios envió a su Hijo unigénito al mundo, para que vivamos por él. En esto consiste el amor: no en que nosotros hayamos amado a Dios, sino en que él nos amó a nosotros, y envió a su Hijo en propiciación por nuestros pecados.",
    "Efesios 2:4-5 - Pero Dios, que es rico en misericordia, por su gran amor con que nos amó, aun estando nosotros muertos en pecados, nos dio vida juntamente con Cristo, (por gracia sois salvos),",
    "1 Juan 3:16 - En esto hemos conocido el amor, en que él puso su vida por nosotros; también nosotros debemos poner nuestras vidas por los hermanos.",
    "1 Pedro 4:8 - Y ante todo, tened entre vosotros ferviente amor; porque el amor cubrirá multitud de pecados.",
    "Salmos 136:26 - Alabad al Dios de los cielos, porque para siempre es su misericordia.",
    "Proverbios 10:12 - El odio despierta contiendas; más el amor cubrirá todas las faltas.",
    "Juan 15:13 - Nadie tiene mayor amor que este, que uno ponga su vida por sus amigos.",
    "Gálatas 5:22-23 - Mas el fruto del Espíritu es amor, gozo, paz, paciencia, benignidad, bondad, fe, mansedumbre, templanza; contra tales cosas no hay ley.",
    "Colosenses 3:14 - Y sobre todas estas cosas vestíos de amor, que es el vínculo perfecto.",
    "Romanos 13:10 - El amor no hace mal al prójimo; así que el cumplimiento de la ley es el amor.",
    "Cantares 8:7 - Las muchas aguas no podrán apagar el amor, ni lo ahogarán los ríos; si diese el hombre todos los bienes de su casa por este amor, de cierto lo menospreciarían.",
    "1 Juan 4:11 - Amados, si Dios nos ha amado así, debemos también nosotros amarnos unos a otros.",
    "Mateo 22:37-39 - Jesús le dijo: Amarás al Señor tu Dios con todo tu corazón, y con toda tu alma, y con toda tu mente. Este es el primero y grande mandamiento. Y el segundo es semejante: Amarás a tu prójimo como a ti mismo.",
    "Efesios 5:2 - Y andar en amor, como también Cristo nos amó, y se entregó a sí mismo por nosotros, ofrenda y sacrificio a Dios en olor fragante.",
    "Hebreos 13:1 - Permanezca el amor fraternal.",
    "2 Corintios 5:14 - Porque el amor de Cristo nos constriñe, pensando esto: que si uno murió por todos, luego todos murieron;",
    "Salmos 103:17 - Mas la misericordia del Señor es desde la eternidad y hasta la eternidad sobre los que le temen, y su justicia sobre los hijos de los hijos."
]

   

    


    

}



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verse/<feeling>')
def show_verse(feeling):
    if feeling in verses:
        verse = random.choice(verses[feeling])
        return render_template('verse.html', verse=verse, feeling=feeling)
    return redirect(url_for('index'))

@app.route('/biblia')
def biblia():
    return render_template('biblia.html')




if __name__ == '__main__':
    app.run(debug=True)
