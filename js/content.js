(function () {
  "use strict";

  const topics = Object.freeze({
    "senior-driving": Object.freeze({
      id: "senior-driving",
      session: "Session I",
      title: "Senior Driver License Renewal in Taiwan",
      subtitle: "Should older drivers face stricter license renewal requirements?",
      summaryParagraphs: Object.freeze([
        "On May 31, 2026, Taiwan lowered the mandatory senior driver license renewal age from 75 to 70.",
        "Drivers aged 70 to 74 must pass a physical examination and complete a road-safety course. Their renewed license remains valid until age 75.",
        "Drivers aged 75 or above must also complete a cognitive assessment, or provide medical evidence showing that they do not have moderate or severe dementia. They must renew their licenses every three years."
      ]),
      factNote: "The policy does not automatically require every older driver to retake an actual road test. Whether a road test should be added is one of the discussion questions.",
      sourceLabel: "Taiwan Directorate General of Highways",
      sourceUrl: "https://www.thb.gov.tw/en/News_Content_Table.aspx?n=10868&s=300330",
      image: Object.freeze({
        src: "images/senior-driving-summary.png",
        alt: "Illustrated English summary of Taiwan's senior driver license renewal rules for ages 70 to 74 and age 75 or older.",
        disclosure: "AI-generated illustrative summary based on the official policy. It is not an official government graphic."
      }),
      questions: Object.freeze([
        "Do you agree that drivers should be required to renew their licenses after the age of 70? Is 70 an appropriate age, or should the requirement begin earlier or later?",
        "Should older drivers be required to retake an actual road test, or are physical examinations, cognitive assessments and road-safety courses enough?",
        "Is it fair to judge driving ability mainly by age? Should a driver’s health, accident history and driving record be considered more important than age?",
        "If you felt that an elderly family member or friend was no longer able to drive safely, would you ask that person to stop driving? Who should make the final decision—the driver, the family, a doctor or the government?",
        "If older people give up driving, what transportation services or financial support should the government provide?"
      ])
    }),

    "mass-tourism": Object.freeze({
      id: "mass-tourism",
      session: "Session II",
      title: "Mass Tourism in Mallorca",
      subtitle: "Is mass tourism destroying the places we love?",
      summaryParagraphs: Object.freeze([
        "On July 26, 2026, residents marched in Mallorca, Spain, to protest against mass tourism.",
        "Protesters said that excessive visitor numbers were damaging the island’s culture and environment and making everyday life more difficult for local residents.",
        "Wider reporting on overtourism in Spain has focused on rising housing costs, crowded streets, pressure on transportation and public services, and heavy demand for water and other natural resources.",
        "Tourism also provides jobs, business income and tax revenue. The central conflict is how to preserve these benefits without making residents and the environment bear most of the costs."
      ]),
      factNote: "The Reuters link is a short news-video page. This summary clearly separates the video’s core report from broader background reporting on overtourism in Spain.",
      sourceLabel: "Reuters video report",
      sourceUrl: "https://www.reuters.com/video/watch/idRW109027072026RP1/",
      backgroundSource: Object.freeze({
        label: "Reuters background article (2024)",
        url: "https://www.reuters.com/world/europe/thousands-protest-spains-mallorca-against-mass-tourism-2024-07-21/"
      }),
      image: Object.freeze({
        src: "images/mass-tourism-article-summary.png",
        alt: "Illustrated English news summary of residents protesting mass tourism in Mallorca and its effects on housing, services, culture and the environment.",
        disclosure: "AI-generated illustrative summary based on Reuters reporting. The people and scenes are not original Reuters photographs."
      }),
      questions: Object.freeze([
        "Do you think mass tourism brings more benefits or more problems to a popular destination? Who benefits the most from tourism, and who suffers the most?",
        "Have you ever visited a place that was so crowded that it affected your travel experience? Did the crowds make you enjoy the trip less?",
        "Should popular destinations limit the number of visitors by requiring reservations, restricting tour buses or cruise ships, or charging higher entrance fees and tourism taxes?",
        "Is it fair for local residents to blame tourists, or should governments and tourism businesses take more responsibility?",
        "Would you be willing to travel during the off-season, visit a less famous destination or pay more money to reduce the negative effects of tourism? Why or why not?"
      ])
    })
  });

  function get(topicId) {
    const topic = topics[topicId];
    if (!topic) {
      throw new Error(`Unknown topic: ${topicId}`);
    }
    return topic;
  }

  window.ClubContent = Object.freeze({ get });
})();
