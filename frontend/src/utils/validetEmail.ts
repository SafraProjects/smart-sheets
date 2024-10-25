const commonDomains = [
  "gmail.com",
  "outlook.com",
  "yahoo.com",
  "hotmail.com",
  "icloud.com",
  "protonmail.com",
  "zoho.com",
  "aol.com",
  "gmx.com",
  "yandex.com",
];

function validateEmail(email: string) {
  // Regex לבדיקת מבנה תקין של אימייל
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return { isValid: false, suggestion: null, message: "Invalid email format." };
  }

  // הפרדה בין שם המשתמש לדומיין
  const [user, domain] = email.split("@");
  if (!domain || !user) {
    return { isValid: false, suggestion: null, message: "Missing domain." };
  }

  // בדוק אם הדומיין קיים ברשימה הנפוצה
  if (commonDomains.includes(domain)) {
    return { isValid: true, suggestion: null, message: "Valid email." };
  }

  // בדוק דומיינים קרובים אם הדומיין לא נמצא ברשימת הדומיינים הנפוצים
  const suggestedDomain = suggestDomain(domain);
  if (suggestedDomain) {
    return {
      isValid: false,
      suggestion: `${user}@${suggestedDomain}`,
      message: `Did you mean: `,
    };
  }

  // אם הדומיין לא נמצא אך אין הצעות קרובות
  return { isValid: true, suggestion: null, message: "Unknown domain." };
}

export default validateEmail;

function suggestDomain(domain: string) {
  // שימוש במרחק Levenshtein כדי למצוא דומיין קרוב
  let closestDomain = null;
  let minDistance = Infinity;

  commonDomains.forEach((commonDomain) => {
    const distance = levenshteinDistance(domain, commonDomain);
    if (distance < minDistance) {
      minDistance = distance;
      closestDomain = commonDomain;
    }
  });

  // אם מרחק קטן מ-3, מציעים את הדומיין הקרוב
  return minDistance < 3 ? closestDomain : null;
}

// פונקציית מרחק Levenshtein
function levenshteinDistance(a: string, b: string) {
  const matrix = Array.from({ length: a.length + 1 }, () => Array(b.length + 1).fill(0));

  for (let i = 0; i <= a.length; i++) {
    matrix[i][0] = i;
  }
  for (let j = 0; j <= b.length; j++) {
    matrix[0][j] = j;
  }

  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1, // מחיקה
        matrix[i][j - 1] + 1, // הוספה
        matrix[i - 1][j - 1] + cost // החלפה
      );
    }
  }

  return matrix[a.length][b.length];
}
