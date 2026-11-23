from amos_layout import PDF
B='https://www.churchofjesuschrist.org/study/'
manual=B+'manual/come-follow-me-for-home-and-church-old-testament-2026/48?lang=eng'
oaks=B+'general-conference/2024/10/18oaks?lang=eng'
teh=B+'general-conference/2026/04/17teh?lang=eng'
helps=B+'manual/scripture-helps-old-testament/46-amos-obadiah-jonah?lang=eng'


def build(destination):
    q=PDF(destination, 'amos-quick-study.pdf','Amos, Obadiah and Jonah: Quick student study')
    q.start('The Lord reveals truth<br/>through His prophets.','Amos, Obadiah & Jonah • Quick path • About 10 minutes')
    q.p('Why would the Lord send a warning people don’t want to hear?',11,'Bold');q.gap(10)
    q.p('Start with a prayer. This companion supports, not replaces, this week’s Come, Follow Me lesson. Your answers can stay private.',10);q.gap(10)
    q.resource('OFFICIAL CHURCH LESSON • SCAN TO OPEN','Come, Follow Me • November 23–29',manual,'Amos; Obadiah; Jonah • ChurchofJesusChrist.org')
    q.head('01 / Read & notice','Sent, not self-appointed.')
    q.link('READ  Amos 7:12–15',B+'scriptures/ot/amos/7?id=p12-p15&lang=eng')
    q.p('For more context, start at verses 10–11. Amaziah tells Amos to take his preaching elsewhere. Listen to Amos’s reason for speaking.',10);q.gap(9)
    q.p('What does Amaziah want Amos to do? What reason does Amos give for speaking anyway?',10.5,'Bold');q.lines(2)
    q.head('02 / Follow the source','A voice with a source.')
    q.link('READ  Amos 3:3–4, 7–8  •  Optional: all of verses 3–8',B+'scriptures/ot/amos/3?id=p3-p8&lang=eng')
    q.p('In verse 8, what explains why Amos speaks? How does verse 7 change the way you hear his warning?',10.5,'Bold');q.lines(2)
    q.p('Notice the source: the Lord speaks. The messenger: Amos is called to prophesy. The response: consider the truth, not just its popularity.',9.5)
    q.end('Quick path')
    q.start('Try hearing it today.','Continue the quick path • A teaching about Jesus, not just an ancient story.')
    q.head('03 / Connect with Christ','What would peacemaking look like?')
    q.link('READ  3 Nephi 11:29–30',B+'scriptures/bofm/3-ne/11?id=p29-p30&lang=eng')
    q.p('What does Jesus ask us to stop stirring up?',10.5,'Bold');q.gap(12)
    q.resource('GENERAL CONFERENCE • PRESIDENT DALLIN H. OAKS','Following Christ',oaks,'In section III, read the paragraph containing “We need to love and do good to all” and the section’s closing paragraph.')
    q.p('OPTIONAL • FICTIONAL GROUP CHAT',8,'Bold');q.gap(6)
    q.p('Someone posts an embarrassing screenshot. People you like pile on.',11,'Serif');q.gap(10)
    q.p('What can you do without adding to the contention?',10.5,'Bold');q.lines(2)
    q.p('Peacemaking is not pretending harm is okay. You could stop sharing the screenshot, support the person being hurt, or involve a trusted adult if there is bullying or danger.',10);q.gap(16)
    q.head('04 / Read, pray, act','Choose one small response.')
    q.p('What is the Lord inviting me to understand or change?',10.5,'Bold');q.gap(8)
    q.p('Choose a passage to reread, a question to pray about, or a good action to try. Write one small step and when you will take it.',10);q.lines(2)
    q.p('Close with prayer. Bring one question or something you noticed to class. You do not need to share private experiences or pretend to have every answer.',10);q.gap(10)
    q.p('You can stop here. The deeper path is optional.',10,'Bold')
    q.end('Quick path');q.save()

    d=PDF(destination, 'amos-deep-study.pdf','Amos, Obadiah and Jonah: Deeper student study')
    d.start('Follow a deeper question.','Amos, Obadiah & Jonah • Optional • Choose one module or explore more.')
    d.p('THE LORD REVEALS TRUTH THROUGH HIS PROPHETS',9,'Bold');d.gap(8)
    d.p('Begin with prayer and the official Come, Follow Me lesson. These modules extend the quick path. Keep personal answers here or in your notebook.',10);d.gap(9)
    d.link('OFFICIAL LESSON  Come, Follow Me • November 23–29',manual)
    d.p('Direct QR links for the lesson and additional sources are on page 3.',9);d.gap(15)
    d.head('A / Why warn?','What does the Lord want for His people?')
    d.link('READ  Amos 5:14–15, 24',B+'scriptures/ot/amos/5?id=p14-p15,p24&lang=eng')
    d.link('READ  Ezekiel 33:7–11',B+'scriptures/ot/ezek/33?id=p7-p11&lang=eng')
    d.p('Look for the action words in each passage. Notice where the watchman receives the warning and what the Lord says He wants for His people.',10);d.gap(9)
    d.p('What does the Lord want people to do, not merely feel?',10.5,'Bold');d.lines(3)
    d.head('B / More than a warning','Christ offers strength, not just instructions.')
    d.link('READ  Alma 7:11–13',B+'scriptures/bofm/alma/7?id=p11-p13&lang=eng')
    d.p('Notice what the Savior takes upon Himself and why. A prophet’s message can reveal the help Jesus Christ offers when life is difficult.',10);d.gap(9)
    d.p('What does Alma teach you about the Savior’s ability to help? How does this widen your picture of a prophet’s message?',10.5,'Bold');d.lines(3)
    d.end('Deeper path')
    d.start('Trace the invitation to Christ.','Continue with one of these optional questions. There is no completion requirement.')
    d.head('C / Follow the links','Where does the teaching lead?')
    d.p('Start in the official lesson’s section “The Lord reveals truth through His prophets.” Follow its link to Elder Michael John U. Teh’s April 2026 message. Find footnote 4 and follow it to President Oaks’s “Following Christ.”',10);d.gap(10)
    d.link('OPEN  Follow the Prophet; He Knows the Way • Elder Teh',teh)
    d.link('OPEN  President Oaks • Following Christ, section III',oaks)
    d.p('Return to 3 Nephi 11:29–30 on purpose: this time compare Christ’s words with the modern invitation rather than simply repeating the reading.',10);d.gap(9)
    d.link('COMPARE  3 Nephi 11:29–30',B+'scriptures/bofm/3-ne/11?id=p29-p30&lang=eng')
    d.p('How does the prophetic invitation lead you back to Jesus Christ?',10.5,'Bold');d.lines(3)
    d.head('D / Optional story connection','Who gets to receive mercy?')
    d.link('READ  Jonah 3:1–5, 10; 4:1–2, 10–11',B+'scriptures/ot/jonah/3?lang=eng')
    d.p('Read how Nineveh responds to a warning, then turn to chapter 4 and notice Jonah’s reaction and the Lord’s response. This is a brief connection, not a second full lesson.',10);d.gap(9)
    d.p('What do the people’s response and the Lord’s mercy add to your understanding of why He sends a warning?',10.5,'Bold');d.lines(3)
    d.p('Close with prayer. Keep one question or insight for class; personal experiences can remain private.',10)
    d.end('Deeper path')
    d.start('Resources you can open from paper.','Scan a code or click an underlined title in the digital PDF.')
    d.p('These are official Church sources. They support your study; you do not need to read every resource. Scripture references throughout can also be found in your scriptures or Gospel Library.',10);d.gap(15)
    for row in [
     ('OFFICIAL CHURCH LESSON','Come, Follow Me • November 23–29',manual,'Amos; Obadiah; Jonah. Begin with the full lesson.'),
     ('OFFICIAL CHURCH STUDY HELP','Scripture Helps: Amos, Obadiah, Jonah',helps,'Background and explanations for this week’s scripture reading.'),
     ('GENERAL CONFERENCE • ELDER MICHAEL JOHN U. TEH','Follow the Prophet; He Knows the Way',teh,'The message linked from the manual. Follow footnote 4 for module C.'),
     ('GENERAL CONFERENCE • PRESIDENT DALLIN H. OAKS','Following Christ • October 2024',oaks,'Section III connects following Jesus Christ with peacemaking.'),
     ('SCRIPTURE • BOOK OF MORMON','Alma 7:11–13',B+'scriptures/bofm/alma/7?id=p11-p13&lang=eng','Christ’s suffering, understanding, and power to help.'),
     ('SCRIPTURE • OLD TESTAMENT','Jonah 3–4',B+'scriptures/ot/jonah/3?lang=eng','For module D: read the selected verses, then go to chapter 4.')]:d.resource(*row)
    d.p('Unofficial supplemental study. Not affiliated with or endorsed by The Church of Jesus Christ of Latter-day Saints.',8)
    d.end('Deeper path');d.save()
